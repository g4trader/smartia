from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ParsedMessage(BaseModel):
    """Standardized message format across all providers"""
    message_id: str
    from_number: str
    timestamp: str
    message_type: str  # text, button, status
    content: str
    button_payload: Optional[str] = None
    provider: str  # meta, twilio, zenvia

class BaseProvider(ABC):
    """Abstract base class for WhatsApp providers"""
    
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
    
    @abstractmethod
    def parse_webhook(self, payload: Dict[str, Any]) -> List[ParsedMessage]:
        """
        Parse webhook payload from provider
        
        Args:
            payload: Raw webhook payload
            
        Returns:
            List of standardized parsed messages
        """
        pass
    
    @abstractmethod
    def send_message(self, to: str, text: str) -> bool:
        """
        Send WhatsApp message
        
        Args:
            to: Recipient phone number
            text: Message text
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def verify_webhook(self, request_data: Dict[str, Any]) -> bool:
        """
        Verify webhook authenticity
        
        Args:
            request_data: Webhook request data
            
        Returns:
            True if webhook is authentic, False otherwise
        """
        pass
