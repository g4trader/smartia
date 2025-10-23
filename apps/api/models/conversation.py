from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .database import Base

class ConversationState(enum.Enum):
    NEW_INTENT = "new_intent"
    ASK_DATE = "ask_date"
    ASK_TIME = "ask_time"
    CONFIRM = "confirm"
    DONE = "done"

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    state = Column(Enum(ConversationState), default=ConversationState.NEW_INTENT)
    intent = Column(String(50), nullable=True)  # agendar, remarcar, cancelar, duvidas
    context_data = Column(Text, nullable=True)  # JSON string with context
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="conversations")
    interactions = relationship("Interaction", back_populates="conversation")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, patient_id={self.patient_id}, state={self.state})>"
