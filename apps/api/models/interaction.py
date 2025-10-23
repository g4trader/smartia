from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .database import Base

class InteractionType(enum.Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    type = Column(Enum(InteractionType), nullable=False)
    message_text = Column(Text, nullable=True)
    message_type = Column(String(20), nullable=True)  # text, button, status
    provider_message_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="interactions")
    patient = relationship("Patient")
    
    def __repr__(self):
        return f"<Interaction(id={self.id}, type={self.type}, text={self.message_text[:50]})>"
