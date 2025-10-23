import os
import requests
from typing import List, Dict, Any, Optional
from .base import BaseProvider, ParsedMessage

class TwilioProvider(BaseProvider):
    """Twilio WhatsApp API provider"""
    
    def __init__(self):
        super().__init__("twilio")
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "")
        self.base_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
    
    def parse_webhook(self, payload: Dict[str, Any]) -> List[ParsedMessage]:
        """Parse Twilio webhook payload"""
        messages = []
        
        try:
            # Twilio sends form data, so payload is already parsed
            message_id = payload.get("MessageSid", "")
            from_number = payload.get("From", "").replace("whatsapp:", "")
            timestamp = payload.get("Timestamp", "")
            body = payload.get("Body", "")
            
            if message_id and from_number and body:
                message = ParsedMessage(
                    message_id=message_id,
                    from_number=from_number,
                    timestamp=timestamp,
                    message_type="text",
                    content=body,
                    provider=self.provider_name
                )
                messages.append(message)
                
        except Exception as e:
            print(f"Error parsing Twilio webhook: {e}")
            
        return messages
    
    def send_message(self, to: str, text: str) -> bool:
        """Send message via Twilio API"""
        try:
            auth = (self.account_sid, self.auth_token)
            
            payload = {
                "From": f"whatsapp:{self.whatsapp_number}",
                "To": f"whatsapp:{to}",
                "Body": text
            }
            
            response = requests.post(self.base_url, auth=auth, data=payload)
            return response.status_code == 201
            
        except Exception as e:
            print(f"Error sending Twilio message: {e}")
            return False
    
    def verify_webhook(self, request_data: Dict[str, Any]) -> bool:
        """Verify Twilio webhook using signature validation"""
        # Twilio webhook verification is more complex and requires signature validation
        # For now, we'll return True (in production, implement proper signature validation)
        return True
