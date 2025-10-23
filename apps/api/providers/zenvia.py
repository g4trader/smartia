import os
import requests
from typing import List, Dict, Any, Optional
from .base import BaseProvider, ParsedMessage

class ZenviaProvider(BaseProvider):
    """Zenvia WhatsApp API provider"""
    
    def __init__(self):
        super().__init__("zenvia")
        self.api_key = os.getenv("ZENVIA_API_KEY", "")
        self.whatsapp_number = os.getenv("ZENVIA_WHATSAPP_NUMBER", "")
        self.base_url = "https://api.zenvia.com/v2/channels/whatsapp/messages"
    
    def parse_webhook(self, payload: Dict[str, Any]) -> List[ParsedMessage]:
        """Parse Zenvia webhook payload"""
        messages = []
        
        try:
            # Zenvia webhook structure
            if "message" in payload:
                message_data = payload["message"]
                message_id = message_data.get("id", "")
                from_number = message_data.get("from", "")
                timestamp = message_data.get("timestamp", "")
                
                # Handle text messages
                if "contents" in message_data:
                    for content in message_data["contents"]:
                        if content.get("type") == "text":
                            message = ParsedMessage(
                                message_id=message_id,
                                from_number=from_number,
                                timestamp=timestamp,
                                message_type="text",
                                content=content.get("text", ""),
                                provider=self.provider_name
                            )
                            messages.append(message)
                            
        except Exception as e:
            print(f"Error parsing Zenvia webhook: {e}")
            
        return messages
    
    def send_message(self, to: str, text: str) -> bool:
        """Send message via Zenvia API"""
        try:
            headers = {
                "X-API-TOKEN": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "from": self.whatsapp_number,
                "to": to,
                "contents": [{"type": "text", "text": text}]
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error sending Zenvia message: {e}")
            return False
    
    def verify_webhook(self, request_data: Dict[str, Any]) -> bool:
        """Verify Zenvia webhook"""
        # Zenvia webhook verification (implement based on their documentation)
        # For now, return True
        return True
