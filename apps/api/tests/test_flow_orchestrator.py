import pytest
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base, Patient, Conversation, ConversationState
from parsers.meta_parser import ParsedMessage
from orchestrator import FlowOrchestrator, WhatsAppService

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Create a test database session"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def mock_whatsapp_service():
    """Create a mock WhatsApp service"""
    service = Mock(spec=WhatsAppService)
    service.send_message.return_value = True
    return service

@pytest.fixture
def orchestrator(db_session, mock_whatsapp_service):
    """Create a FlowOrchestrator instance for testing"""
    return FlowOrchestrator(db_session, mock_whatsapp_service)

class TestFlowOrchestrator:
    
    def test_get_or_create_patient_new(self, orchestrator):
        """Test creating a new patient"""
        phone_number = "5511999999999"
        
        patient = orchestrator._get_or_create_patient(phone_number)
        
        assert patient.phone_number == phone_number
        assert patient.id is not None
    
    def test_get_or_create_patient_existing(self, orchestrator, db_session):
        """Test getting an existing patient"""
        phone_number = "5511999999999"
        
        # Create patient first
        patient1 = orchestrator._get_or_create_patient(phone_number)
        db_session.commit()
        
        # Get the same patient
        patient2 = orchestrator._get_or_create_patient(phone_number)
        
        assert patient1.id == patient2.id
        assert patient2.phone_number == phone_number
    
    def test_get_or_create_conversation_new(self, orchestrator, db_session):
        """Test creating a new conversation"""
        phone_number = "5511999999999"
        patient = orchestrator._get_or_create_patient(phone_number)
        db_session.commit()
        
        conversation = orchestrator._get_or_create_conversation(patient.id)
        
        assert conversation.patient_id == patient.id
        assert conversation.state == ConversationState.NEW_INTENT
    
    def test_process_message_new_intent(self, orchestrator, db_session):
        """Test processing a new intent message"""
        phone_number = "5511999999999"
        parsed_message = ParsedMessage(
            message_id="test123",
            from_number=phone_number,
            timestamp="1640995200",
            message_type="text",
            content="Quero agendar uma consulta"
        )
        
        success = orchestrator.process_message(parsed_message)
        
        assert success is True
        
        # Check that patient was created
        patient = db_session.query(Patient).filter(Patient.phone_number == phone_number).first()
        assert patient is not None
        
        # Check that conversation was created
        conversation = db_session.query(Conversation).filter(
            Conversation.patient_id == patient.id
        ).first()
        assert conversation is not None
        assert conversation.intent == "agendar"
        assert conversation.state == ConversationState.ASK_DATE
    
    def test_process_message_date_response(self, orchestrator, db_session):
        """Test processing a date response"""
        phone_number = "5511999999999"
        
        # Create patient and conversation in ASK_DATE state
        patient = orchestrator._get_or_create_patient(phone_number)
        conversation = orchestrator._get_or_create_conversation(patient.id)
        conversation.state = ConversationState.ASK_DATE
        conversation.intent = "agendar"
        db_session.commit()
        
        parsed_message = ParsedMessage(
            message_id="test123",
            from_number=phone_number,
            timestamp="1640995200",
            message_type="text",
            content="15/12/2024"
        )
        
        success = orchestrator.process_message(parsed_message)
        
        assert success is True
        
        # Check that conversation state changed to ASK_TIME
        db_session.refresh(conversation)
        assert conversation.state == ConversationState.ASK_TIME
        
        # Check that date was stored in context
        import json
        context = json.loads(conversation.context_data)
        assert context["selected_date"] == "15/12/2024"
    
    def test_process_message_time_response(self, orchestrator, db_session):
        """Test processing a time response"""
        phone_number = "5511999999999"
        
        # Create patient and conversation in ASK_TIME state
        patient = orchestrator._get_or_create_patient(phone_number)
        conversation = orchestrator._get_or_create_conversation(patient.id)
        conversation.state = ConversationState.ASK_TIME
        conversation.intent = "agendar"
        conversation.context_data = '{"selected_date": "15/12/2024"}'
        db_session.commit()
        
        parsed_message = ParsedMessage(
            message_id="test123",
            from_number=phone_number,
            timestamp="1640995200",
            message_type="text",
            content="14:30"
        )
        
        success = orchestrator.process_message(parsed_message)
        
        assert success is True
        
        # Check that conversation state changed to CONFIRM
        db_session.refresh(conversation)
        assert conversation.state == ConversationState.CONFIRM
        
        # Check that time was stored in context
        import json
        context = json.loads(conversation.context_data)
        assert context["selected_time"] == "14:30"
    
    def test_process_message_confirmation_yes(self, orchestrator, db_session):
        """Test processing a positive confirmation"""
        phone_number = "5511999999999"
        
        # Create patient and conversation in CONFIRM state
        patient = orchestrator._get_or_create_patient(phone_number)
        conversation = orchestrator._get_or_create_conversation(patient.id)
        conversation.state = ConversationState.CONFIRM
        conversation.intent = "agendar"
        conversation.context_data = '{"selected_date": "15/12/2024", "selected_time": "14:30"}'
        db_session.commit()
        
        parsed_message = ParsedMessage(
            message_id="test123",
            from_number=phone_number,
            timestamp="1640995200",
            message_type="text",
            content="sim"
        )
        
        success = orchestrator.process_message(parsed_message)
        
        assert success is True
        
        # Check that conversation state changed to DONE
        db_session.refresh(conversation)
        assert conversation.state == ConversationState.DONE
