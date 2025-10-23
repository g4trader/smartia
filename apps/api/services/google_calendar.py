import os
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .base_calendar import BaseCalendarService, TimeSlot, CalendarEvent

# Scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarService(BaseCalendarService):
    """Google Calendar service implementation"""
    
    def __init__(self, credentials_path: Optional[str] = None, token_path: Optional[str] = None):
        self.credentials_path = credentials_path or os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
        self.token_path = token_path or os.getenv("GOOGLE_TOKEN_PATH", "token.json")
        self.calendar_id = os.getenv("GOOGLE_CALENDAR_ID", "primary")
        self.timezone = os.getenv("CLINIC_TIMEZONE", "America/Sao_Paulo")
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(f"Credentials file not found: {self.credentials_path}")
                
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def list_slots(self, start_date: datetime, end_date: datetime, duration_minutes: int = 60) -> List[TimeSlot]:
        """List available time slots in a date range"""
        try:
            # Convert to timezone-aware datetimes
            tz = pytz.timezone(self.timezone)
            start_date = tz.localize(start_date) if start_date.tzinfo is None else start_date
            end_date = tz.localize(end_date) if end_date.tzinfo is None else end_date
            
            # Get existing events in the time range
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_date.isoformat(),
                timeMax=end_date.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Generate time slots
            slots = []
            current = start_date
            
            while current < end_date:
                slot_end = current + timedelta(minutes=duration_minutes)
                
                # Check if slot conflicts with existing events
                is_available = not self._has_conflict(current, slot_end, events)
                
                slot = TimeSlot(
                    start=current,
                    end=slot_end,
                    available=is_available
                )
                slots.append(slot)
                
                current += timedelta(minutes=30)  # 30-minute intervals
            
            return slots
            
        except HttpError as error:
            print(f"Error listing slots: {error}")
            return []
    
    def book_slot(self, slot: TimeSlot, event: CalendarEvent) -> Optional[str]:
        """Book a time slot by creating an event"""
        try:
            # Convert to timezone-aware datetimes
            tz = pytz.timezone(self.timezone)
            start = tz.localize(event.start) if event.start.tzinfo is None else event.start
            end = tz.localize(event.end) if event.end.tzinfo is None else event.end
            
            # Create event body
            event_body = {
                'summary': event.title,
                'description': event.description or '',
                'start': {
                    'dateTime': start.isoformat(),
                    'timeZone': self.timezone,
                },
                'end': {
                    'dateTime': end.isoformat(),
                    'timeZone': self.timezone,
                },
            }
            
            # Add attendees if provided
            if event.attendees:
                event_body['attendees'] = [{'email': email} for email in event.attendees]
            
            # Add metadata if provided
            if event.metadata:
                event_body['extendedProperties'] = {
                    'private': event.metadata
                }
            
            # Create the event
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event_body
            ).execute()
            
            return created_event.get('id')
            
        except HttpError as error:
            print(f"Error booking slot: {error}")
            return None
    
    def cancel_event(self, event_id: str) -> bool:
        """Cancel an existing event"""
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            return True
            
        except HttpError as error:
            print(f"Error canceling event: {error}")
            return False
    
    def get_event(self, event_id: str) -> Optional[CalendarEvent]:
        """Get event details by ID"""
        try:
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            return self._parse_event(event)
            
        except HttpError as error:
            print(f"Error getting event: {error}")
            return None
    
    def update_event(self, event_id: str, event: CalendarEvent) -> bool:
        """Update an existing event"""
        try:
            # Convert to timezone-aware datetimes
            tz = pytz.timezone(self.timezone)
            start = tz.localize(event.start) if event.start.tzinfo is None else event.start
            end = tz.localize(event.end) if event.end.tzinfo is None else event.end
            
            # Create event body
            event_body = {
                'summary': event.title,
                'description': event.description or '',
                'start': {
                    'dateTime': start.isoformat(),
                    'timeZone': self.timezone,
                },
                'end': {
                    'dateTime': end.isoformat(),
                    'timeZone': self.timezone,
                },
            }
            
            # Add attendees if provided
            if event.attendees:
                event_body['attendees'] = [{'email': email} for email in event.attendees]
            
            # Add metadata if provided
            if event.metadata:
                event_body['extendedProperties'] = {
                    'private': event.metadata
                }
            
            # Update the event
            self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event_body
            ).execute()
            
            return True
            
        except HttpError as error:
            print(f"Error updating event: {error}")
            return False
    
    def _has_conflict(self, start: datetime, end: datetime, events: List[Dict]) -> bool:
        """Check if a time slot conflicts with existing events"""
        for event in events:
            event_start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            event_end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
            
            # Check for overlap
            if (start < event_end and end > event_start):
                return True
        
        return False
    
    def _parse_event(self, event: Dict) -> CalendarEvent:
        """Parse Google Calendar event to CalendarEvent"""
        start_str = event['start'].get('dateTime', event['start'].get('date'))
        end_str = event['end'].get('dateTime', event['end'].get('date'))
        
        # Parse datetime strings
        start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
        
        # Extract attendees
        attendees = []
        if 'attendees' in event:
            attendees = [attendee['email'] for attendee in event['attendees']]
        
        # Extract metadata
        metadata = {}
        if 'extendedProperties' in event and 'private' in event['extendedProperties']:
            metadata = event['extendedProperties']['private']
        
        return CalendarEvent(
            id=event['id'],
            title=event.get('summary', ''),
            start=start,
            end=end,
            description=event.get('description', ''),
            attendees=attendees,
            metadata=metadata
        )
