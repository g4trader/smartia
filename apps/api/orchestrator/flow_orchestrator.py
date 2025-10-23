import json
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models import Patient, Conversation, Interaction, ConversationState, Appointment, AppointmentStatus
from models.interaction import InteractionType
from parsers.meta_parser import ParsedMessage
from .whatsapp_service import WhatsAppService
from services import BaseCalendarService
from services.base_calendar import CalendarEvent

class FlowOrchestrator:
    """Orchestrates conversation flows for WhatsApp interactions"""
    
    def __init__(self, db: Session, whatsapp_service: WhatsAppService, calendar_service: Optional[BaseCalendarService] = None):
        self.db = db
        self.whatsapp_service = whatsapp_service
        self.calendar_service = calendar_service
    
    def process_message(self, parsed_message: ParsedMessage) -> bool:
        """
        Process incoming message and orchestrate conversation flow
        
        Args:
            parsed_message: Parsed message from webhook
            
        Returns:
            bool: True if processed successfully
        """
        try:
            # Get or create patient
            patient = self._get_or_create_patient(parsed_message.from_number)
            
            # Get or create conversation
            conversation = self._get_or_create_conversation(patient.id)
            
            # Save interaction
            self._save_interaction(conversation.id, patient.id, parsed_message)
            
            # Process based on conversation state
            self._process_conversation_state(conversation, parsed_message)
            
            self.db.commit()
            return True
            
        except Exception as e:
            print(f"Error processing message: {e}")
            self.db.rollback()
            return False
    
    def _get_or_create_patient(self, phone_number: str) -> Patient:
        """Get existing patient or create new one"""
        patient = self.db.query(Patient).filter(Patient.phone_number == phone_number).first()
        
        if not patient:
            patient = Patient(phone_number=phone_number)
            self.db.add(patient)
            self.db.flush()  # Get the ID
            
        return patient
    
    def _get_or_create_conversation(self, patient_id: int) -> Conversation:
        """Get active conversation or create new one"""
        # Look for active conversation (not DONE)
        conversation = self.db.query(Conversation).filter(
            Conversation.patient_id == patient_id,
            Conversation.state != ConversationState.DONE
        ).first()
        
        if not conversation:
            conversation = Conversation(
                patient_id=patient_id,
                state=ConversationState.NEW_INTENT
            )
            self.db.add(conversation)
            self.db.flush()
            
        return conversation
    
    def _save_interaction(self, conversation_id: int, patient_id: int, parsed_message: ParsedMessage):
        """Save interaction to database"""
        interaction = Interaction(
            conversation_id=conversation_id,
            patient_id=patient_id,
            type=InteractionType.INCOMING,
            message_text=parsed_message.content,
            message_type=parsed_message.message_type,
            provider_message_id=parsed_message.message_id
        )
        self.db.add(interaction)
    
    def _process_conversation_state(self, conversation: Conversation, parsed_message: ParsedMessage):
        """Process conversation based on current state"""
        if conversation.state == ConversationState.NEW_INTENT:
            self._handle_new_intent(conversation, parsed_message)
        elif conversation.state == ConversationState.ASK_DATE:
            self._handle_date_response(conversation, parsed_message)
        elif conversation.state == ConversationState.ASK_TIME:
            self._handle_time_response(conversation, parsed_message)
        elif conversation.state == ConversationState.CONFIRM:
            self._handle_confirmation(conversation, parsed_message)
    
    def _handle_new_intent(self, conversation: Conversation, parsed_message: ParsedMessage):
        """Handle new intent detection"""
        from ..parsers.meta_parser import MetaWebhookParser
        
        intent = MetaWebhookParser.detect_intent(parsed_message.content)
        conversation.intent = intent
        
        if intent == "agendar":
            conversation.state = ConversationState.ASK_DATE
            self._send_message(conversation.patient.phone_number, 
                             "Ótimo! Vou te ajudar a agendar uma consulta. "
                             "Qual data você prefere? (ex: 15/12/2024)")
        elif intent == "remarcar":
            conversation.state = ConversationState.ASK_DATE
            self._send_message(conversation.patient.phone_number,
                             "Entendi que você quer remarcar. "
                             "Qual nova data você prefere? (ex: 15/12/2024)")
        elif intent == "cancelar":
            conversation.state = ConversationState.DONE
            self._send_message(conversation.patient.phone_number,
                             "Consulta cancelada com sucesso. "
                             "Se precisar reagendar, é só me avisar!")
        elif intent == "duvidas":
            conversation.state = ConversationState.DONE
            self._send_message(conversation.patient.phone_number,
                             "Claro! Posso te ajudar com informações sobre: "
                             "• Horários de funcionamento\n"
                             "• Valores das consultas\n"
                             "• Especialidades disponíveis\n"
                             "• Localização da clínica\n\n"
                             "O que você gostaria de saber?")
    
    def _handle_date_response(self, conversation: Conversation, parsed_message: ParsedMessage):
        """Handle date selection response"""
        # Simple date parsing (in real implementation, use proper date parsing)
        date_text = parsed_message.content.strip()
        
        # Store date in context
        context = self._get_context(conversation)
        context["selected_date"] = date_text
        conversation.context_data = json.dumps(context)
        
        conversation.state = ConversationState.ASK_TIME
        self._send_message(conversation.patient.phone_number,
                         f"Perfeito! Data {date_text} anotada. "
                         "Agora me diga que horário você prefere? "
                         "(ex: 14:30 ou 2:30 da tarde)")
    
    def _handle_time_response(self, conversation: Conversation, parsed_message: ParsedMessage):
        """Handle time selection response"""
        time_text = parsed_message.content.strip()
        
        # Store time in context
        context = self._get_context(conversation)
        context["selected_time"] = time_text
        conversation.context_data = json.dumps(context)
        
        conversation.state = ConversationState.CONFIRM
        
        # Get stored date
        date = context.get("selected_date", "data selecionada")
        
        self._send_message(conversation.patient.phone_number,
                         f"Vou confirmar seu agendamento:\n\n"
                         f"📅 Data: {date}\n"
                         f"🕐 Horário: {time_text}\n\n"
                         f"Está correto? Responda 'sim' para confirmar ou 'não' para alterar.")
    
    def _handle_confirmation(self, conversation: Conversation, parsed_message: ParsedMessage):
        """Handle confirmation response"""
        response = parsed_message.content.lower().strip()
        
        if response in ["sim", "s", "yes", "confirmo", "ok"]:
            # Integrate with calendar service
            context = self._get_context(conversation)
            date = context.get("selected_date", "")
            time = context.get("selected_time", "")
            
            # Try to book the appointment
            event_id = self._book_appointment(conversation, date, time)
            
            if event_id:
                conversation.state = ConversationState.DONE
                self._send_message(conversation.patient.phone_number,
                                 f"✅ Agendamento confirmado!\n\n"
                                 f"📅 Data: {date}\n"
                                 f"🕐 Horário: {time}\n"
                                 f"🆔 ID: {event_id}\n\n"
                                 f"Você receberá um lembrete 24h antes da consulta. "
                                 f"Se precisar de algo, é só me avisar!")
            else:
                self._send_message(conversation.patient.phone_number,
                                 f"❌ Desculpe, não foi possível confirmar o agendamento. "
                                 f"O horário pode ter sido ocupado. "
                                 f"Vamos tentar outro horário?")
        else:
            # Restart the flow
            conversation.state = ConversationState.ASK_DATE
            self._send_message(conversation.patient.phone_number,
                             "Sem problemas! Vamos começar novamente. "
                             "Qual data você prefere? (ex: 15/12/2024)")
    
    def _get_context(self, conversation: Conversation) -> Dict[str, Any]:
        """Get conversation context as dictionary"""
        if conversation.context_data:
            try:
                return json.loads(conversation.context_data)
            except:
                pass
        return {}
    
    def _send_message(self, phone_number: str, text: str):
        """Send WhatsApp message and save interaction"""
        success = self.whatsapp_service.send_message(phone_number, text)
        
        if success:
            # Save outgoing interaction
            # Note: In a real implementation, you'd get the message ID from the API response
            interaction = Interaction(
                conversation_id=None,  # Will be set by the caller
                patient_id=None,       # Will be set by the caller
                type=InteractionType.OUTGOING,
                message_text=text,
                message_type="text"
            )
            self.db.add(interaction)
        
        return success
    
    def _book_appointment(self, conversation: Conversation, date_str: str, time_str: str) -> Optional[str]:
        """Book an appointment using the calendar service"""
        if not self.calendar_service:
            print("No calendar service configured")
            return None
        
        try:
            # Parse date and time (simple parsing - in production, use proper date parsing)
            from datetime import datetime
            import re
            
            # Simple date parsing (DD/MM/YYYY)
            date_match = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_str)
            if not date_match:
                print(f"Invalid date format: {date_str}")
                return None
            
            day, month, year = map(int, date_match.groups())
            
            # Simple time parsing (HH:MM or H:MM)
            time_match = re.match(r'(\d{1,2}):(\d{2})', time_str)
            if not time_match:
                print(f"Invalid time format: {time_str}")
                return None
            
            hour, minute = map(int, time_match.groups())
            
            # Create datetime objects
            start_datetime = datetime(year, month, day, hour, minute)
            end_datetime = start_datetime + timedelta(hours=1)  # 1-hour appointment
            
            # Create calendar event
            event = CalendarEvent(
                title=f"Consulta - {conversation.patient.name or 'Paciente'}",
                start=start_datetime,
                end=end_datetime,
                description=f"Consulta agendada via WhatsApp\nPaciente: {conversation.patient.phone_number}",
                metadata={
                    "patient_id": conversation.patient.id,
                    "conversation_id": conversation.id,
                    "source": "whatsapp"
                }
            )
            
            # Book the slot
            event_id = self.calendar_service.book_slot(None, event)  # No specific slot needed
            
            if event_id:
                # Store event ID in conversation context
                context = self._get_context(conversation)
                context["event_id"] = event_id
                conversation.context_data = json.dumps(context)
                
                # Create appointment record
                appointment = Appointment(
                    patient_id=conversation.patient.id,
                    conversation_id=conversation.id,
                    calendar_event_id=event_id,
                    title=event.title,
                    description=event.description,
                    appointment_date=start_datetime,
                    duration_minutes=60,
                    status=AppointmentStatus.SCHEDULED
                )
                self.db.add(appointment)
            
            return event_id
            
        except Exception as e:
            print(f"Error booking appointment: {e}")
            return None
