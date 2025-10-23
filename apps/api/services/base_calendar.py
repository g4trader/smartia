from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

class TimeSlot(BaseModel):
    """Represents an available time slot"""
    start: datetime
    end: datetime
    available: bool = True
    metadata: Optional[Dict[str, Any]] = None

class CalendarEvent(BaseModel):
    """Represents a calendar event"""
    id: Optional[str] = None
    title: str
    start: datetime
    end: datetime
    description: Optional[str] = None
    attendees: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseCalendarService(ABC):
    """Abstract base class for calendar services"""
    
    @abstractmethod
    def list_slots(self, start_date: datetime, end_date: datetime, duration_minutes: int = 60) -> List[TimeSlot]:
        """
        List available time slots in a date range
        
        Args:
            start_date: Start of the date range
            end_date: End of the date range
            duration_minutes: Duration of each slot in minutes
            
        Returns:
            List of available time slots
        """
        pass
    
    @abstractmethod
    def book_slot(self, slot: TimeSlot, event: CalendarEvent) -> Optional[str]:
        """
        Book a time slot by creating an event
        
        Args:
            slot: The time slot to book
            event: Event details
            
        Returns:
            Event ID if successful, None otherwise
        """
        pass
    
    @abstractmethod
    def cancel_event(self, event_id: str) -> bool:
        """
        Cancel an existing event
        
        Args:
            event_id: ID of the event to cancel
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_event(self, event_id: str) -> Optional[CalendarEvent]:
        """
        Get event details by ID
        
        Args:
            event_id: ID of the event
            
        Returns:
            Event details if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_event(self, event_id: str, event: CalendarEvent) -> bool:
        """
        Update an existing event
        
        Args:
            event_id: ID of the event to update
            event: New event details
            
        Returns:
            True if successful, False otherwise
        """
        pass
