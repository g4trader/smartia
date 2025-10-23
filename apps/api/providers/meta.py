import os
import requests
from typing import List, Dict, Any, Optional
from .base import BaseProvider, ParsedMessage

class MetaProvider(BaseProvider):
    """Meta WhatsApp Cloud API provider"""
    
    def __init__(self):
        super().__init__("meta")
        self.access_token = os.getenv("META_ACCESS_TOKEN", "")
        self.phone_number_id = os.getenv("META_PHONE_NUMBER_ID", "")
        self.verify_token = os.getenv("META_VERIFY_TOKEN", "")
        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
    
    def parse_webhook(self, payload: Dict[str, Any]) -> List[ParsedMessage]:
        """Parse Meta webhook payload"""
        messages = []
        
        try:
            if "entry" in payload:
                for entry in payload["entry"]:
                    for change in entry.get("changes", []):
                        if change.get("field") == "messages":
                            value = change.get("value", {})
                            
                            # Parse incoming messages
                            if "messages" in value:
                                for msg_data in value["messages"]:
                                    message = self._parse_message(msg_data)
                                    if message:
                                        messages.append(message)
                            
                            # Parse message statuses
                            if "statuses" in value:
                                for status_data in value["statuses"]:
                                    message = self._parse_status(status_data)
                                    if message:
                                        messages.append(message)
                                        
        except Exception as e:
            print(f"Error parsing Meta webhook: {e}")
            
        return messages
    
    def _parse_message(self, msg_data: Dict[str, Any]) -> Optional[ParsedMessage]:
        """Parse individual message from Meta payload"""
        try:
            message_id = msg_data.get("id", "")
            from_number = msg_data.get("from", "")
            timestamp = msg_data.get("timestamp", "")
            
            # Handle text messages
            if "text" in msg_data:
                return ParsedMessage(
                    message_id=message_id,
                    from_number=from_number,
                    timestamp=timestamp,
                    message_type="text",
                    content=msg_data["text"].get("body", ""),
                    provider=self.provider_name
                )
            
            # Handle button responses
            if "button" in msg_data:
                button_data = msg_data["button"]
                return ParsedMessage(
                    message_id=message_id,
                    from_number=from_number,
                    timestamp=timestamp,
                    message_type="button",
                    content=button_data.get("text", ""),
                    button_payload=button_data.get("payload", ""),
                    provider=self.provider_name
                )
                
        except Exception as e:
            print(f"Error parsing Meta message: {e}")
            
        return None
    
    def _parse_status(self, status_data: Dict[str, Any]) -> Optional[ParsedMessage]:
        """Parse message status from Meta payload"""
        try:
            message_id = status_data.get("id", "")
            from_number = status_data.get("recipient_id", "")
            timestamp = status_data.get("timestamp", "")
            status = status_data.get("status", "")
            
            return ParsedMessage(
                message_id=message_id,
                from_number=from_number,
                timestamp=timestamp,
                message_type="status",
                content=status,
                provider=self.provider_name
            )
            
        except Exception as e:
            print(f"Error parsing Meta status: {e}")
            
        return None
    
    def send_message(self, to: str, text: str) -> bool:
        """Send message via Meta Cloud API"""
        try:
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
            
        except Exception as e:
            print(f"Error sending Meta message: {e}")
            return False
    
    def verify_webhook(self, request_data: Dict[str, Any]) -> bool:
        """Verify Meta webhook"""
        mode = request_data.get("hub.mode", "")
        token = request_data.get("hub.verify_token", "")
        challenge = request_data.get("hub.challenge", "")
        
        return mode == "subscribe" and token == self.verify_token
