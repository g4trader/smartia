import os
import requests
from typing import Optional

class WhatsAppService:
    """Service for sending WhatsApp messages via different providers"""
    
    def __init__(self, provider: str = "META"):
        self.provider = provider.upper()
        self.access_token = self._get_access_token()
        self.base_url = self._get_base_url()
    
    def _get_access_token(self) -> str:
        """Get access token based on provider"""
        if self.provider == "META":
            return os.getenv("META_ACCESS_TOKEN", "")
        elif self.provider == "TWILIO":
            return os.getenv("TWILIO_AUTH_TOKEN", "")
        elif self.provider == "ZENVIA":
            return os.getenv("ZENVIA_API_KEY", "")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _get_base_url(self) -> str:
        """Get base URL based on provider"""
        if self.provider == "META":
            phone_number_id = os.getenv("META_PHONE_NUMBER_ID", "")
            return f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
        elif self.provider == "TWILIO":
            account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
            return f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        elif self.provider == "ZENVIA":
            return "https://api.zenvia.com/v2/channels/whatsapp/messages"
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def send_message(self, to: str, text: str) -> bool:
        """
        Send WhatsApp message
        
        Args:
            to: Recipient phone number (with country code, no +)
            text: Message text
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.provider == "META":
                return self._send_meta_message(to, text)
            elif self.provider == "TWILIO":
                return self._send_twilio_message(to, text)
            elif self.provider == "ZENVIA":
                return self._send_zenvia_message(to, text)
            else:
                print(f"Unsupported provider: {self.provider}")
                return False
                
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False
    
    def _send_meta_message(self, to: str, text: str) -> bool:
        """Send message via Meta Cloud API"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text}
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.status_code == 200
    
    def _send_twilio_message(self, to: str, text: str) -> bool:
        """Send message via Twilio API"""
        account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        from_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "")
        
        auth = (account_sid, self.access_token)
        
        payload = {
            "From": f"whatsapp:{from_number}",
            "To": f"whatsapp:{to}",
            "Body": text
        }
        
        response = requests.post(self.base_url, auth=auth, data=payload)
        return response.status_code == 201
    
    def _send_zenvia_message(self, to: str, text: str) -> bool:
        """Send message via Zenvia API"""
        headers = {
            "X-API-TOKEN": self.access_token,
            "Content-Type": "application/json"
        }
        
        payload = {
            "from": os.getenv("ZENVIA_WHATSAPP_NUMBER", ""),
            "to": to,
            "contents": [{"type": "text", "text": text}]
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload)
        return response.status_code == 200
