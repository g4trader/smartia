from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import json

class MetaMessage(BaseModel):
    id: str
    from_: str
    timestamp: str
    text: Optional[Dict[str, str]] = None
    button: Optional[Dict[str, Any]] = None
    statuses: Optional[List[Dict[str, Any]]] = None

class MetaEntry(BaseModel):
    id: str
    changes: List[Dict[str, Any]]

class MetaWebhookPayload(BaseModel):
    object: str
    entry: List[MetaEntry]

class ParsedMessage(BaseModel):
    message_id: str
    from_number: str
    timestamp: str
    message_type: str  # text, button, status
    content: str
    button_payload: Optional[str] = None

class MetaWebhookParser:
    """Parser for Meta WhatsApp Cloud API webhook payloads"""
    
    @staticmethod
    def parse_webhook(payload: Dict[str, Any]) -> List[ParsedMessage]:
        """
        Parse Meta webhook payload and extract messages
        
        Args:
            payload: Raw webhook payload from Meta
            
        Returns:
            List of parsed messages
        """
        messages = []
        
        try:
            webhook_data = MetaWebhookPayload(**payload)
            
            for entry in webhook_data.entry:
                for change in entry.changes:
                    if change.get("field") == "messages":
                        value = change.get("value", {})
                        
                        # Parse incoming messages
                        if "messages" in value:
                            for msg_data in value["messages"]:
                                message = MetaWebhookParser._parse_message(msg_data)
                                if message:
                                    messages.append(message)
                        
                        # Parse message statuses (delivered, read, etc.)
                        if "statuses" in value:
                            for status_data in value["statuses"]:
                                message = MetaWebhookParser._parse_status(status_data)
                                if message:
                                    messages.append(message)
                                    
        except Exception as e:
            print(f"Error parsing Meta webhook: {e}")
            
        return messages
    
    @staticmethod
    def _parse_message(msg_data: Dict[str, Any]) -> Optional[ParsedMessage]:
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
                    content=msg_data["text"].get("body", "")
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
                    button_payload=button_data.get("payload", "")
                )
                
        except Exception as e:
            print(f"Error parsing message: {e}")
            
        return None
    
    @staticmethod
    def _parse_status(status_data: Dict[str, Any]) -> Optional[ParsedMessage]:
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
                content=status
            )
            
        except Exception as e:
            print(f"Error parsing status: {e}")
            
        return None
    
    @staticmethod
    def detect_intent(message_text: str) -> str:
        """
        Detect user intent from message text
        
        Args:
            message_text: User's message text
            
        Returns:
            Intent: agendar, remarcar, cancelar, duvidas
        """
        text = message_text.lower().strip()
        
        # Keywords for scheduling
        agendar_keywords = ["agendar", "marcar", "consulta", "horário", "disponível", "quero marcar"]
        remarcar_keywords = ["remarcar", "reagendar", "mudar", "alterar", "trocar"]
        cancelar_keywords = ["cancelar", "desmarcar", "não posso", "não vou"]
        duvidas_keywords = ["dúvida", "pergunta", "como", "quando", "onde", "preço", "valor"]
        
        # Check for cancellation first (most specific)
        if any(keyword in text for keyword in cancelar_keywords):
            return "cancelar"
        # Check for rescheduling
        elif any(keyword in text for keyword in remarcar_keywords):
            return "remarcar"
        # Check for questions
        elif any(keyword in text for keyword in duvidas_keywords):
            return "duvidas"
        # Check for scheduling
        elif any(keyword in text for keyword in agendar_keywords):
            return "agendar"
        else:
            return "agendar"  # Default to scheduling
