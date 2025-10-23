import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Appointment, AppointmentStatus, Patient, Interaction
from models.interaction import InteractionType
from providers.factory import ProviderFactory
from orchestrator import WhatsAppService

class ReminderJob:
    """Job for sending appointment reminders and handling no-shows"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv("DATABASE_URL", "sqlite:///./smartia.db")
        self.engine = create_engine(self.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = SessionLocal()
        
        # Initialize WhatsApp service
        try:
            self.whatsapp_service = WhatsAppService(provider="META")
        except Exception as e:
            print(f"Warning: WhatsApp service not available: {e}")
            self.whatsapp_service = None
    
    def send_reminders_24h(self) -> Dict[str, Any]:
        """Send reminders 24 hours before appointments"""
        try:
            # Find appointments 24 hours from now
            tomorrow = datetime.now() + timedelta(hours=24)
            start_time = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            end_time = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            appointments = self.db.query(Appointment).filter(
                Appointment.appointment_date >= start_time,
                Appointment.appointment_date <= end_time,
                Appointment.status == AppointmentStatus.SCHEDULED
            ).all()
            
            sent_count = 0
            failed_count = 0
            
            for appointment in appointments:
                if self._send_reminder(appointment, "24h"):
                    sent_count += 1
                else:
                    failed_count += 1
            
            return {
                "job": "24h_reminders",
                "timestamp": datetime.now().isoformat(),
                "appointments_found": len(appointments),
                "reminders_sent": sent_count,
                "reminders_failed": failed_count,
                "success": True
            }
            
        except Exception as e:
            return {
                "job": "24h_reminders",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "success": False
            }
    
    def send_reminders_2h(self) -> Dict[str, Any]:
        """Send reminders 2 hours before appointments"""
        try:
            # Find appointments 2 hours from now
            in_2h = datetime.now() + timedelta(hours=2)
            start_time = in_2h.replace(minute=0, second=0, microsecond=0)
            end_time = in_2h.replace(minute=59, second=59, microsecond=999999)
            
            appointments = self.db.query(Appointment).filter(
                Appointment.appointment_date >= start_time,
                Appointment.appointment_date <= end_time,
                Appointment.status == AppointmentStatus.SCHEDULED
            ).all()
            
            sent_count = 0
            failed_count = 0
            
            for appointment in appointments:
                if self._send_reminder(appointment, "2h"):
                    sent_count += 1
                else:
                    failed_count += 1
            
            return {
                "job": "2h_reminders",
                "timestamp": datetime.now().isoformat(),
                "appointments_found": len(appointments),
                "reminders_sent": sent_count,
                "reminders_failed": failed_count,
                "success": True
            }
            
        except Exception as e:
            return {
                "job": "2h_reminders",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "success": False
            }
    
    def handle_no_shows(self) -> Dict[str, Any]:
        """Mark appointments as no-show and send re-engagement messages"""
        try:
            # Find appointments that should have started but patient didn't show up
            now = datetime.now()
            one_hour_ago = now - timedelta(hours=1)
            
            no_show_appointments = self.db.query(Appointment).filter(
                Appointment.appointment_date <= one_hour_ago,
                Appointment.status == AppointmentStatus.SCHEDULED
            ).all()
            
            processed_count = 0
            reengagement_sent = 0
            
            for appointment in no_show_appointments:
                # Mark as no-show
                appointment.status = AppointmentStatus.NO_SHOW
                self.db.commit()
                
                # Send re-engagement message
                if self._send_reengagement_message(appointment):
                    reengagement_sent += 1
                
                processed_count += 1
            
            return {
                "job": "no_show_handler",
                "timestamp": datetime.now().isoformat(),
                "no_shows_found": len(no_show_appointments),
                "processed": processed_count,
                "reengagement_sent": reengagement_sent,
                "success": True
            }
            
        except Exception as e:
            return {
                "job": "no_show_handler",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "success": False
            }
    
    def _send_reminder(self, appointment: Appointment, reminder_type: str) -> bool:
        """Send reminder message for an appointment"""
        if not self.whatsapp_service:
            return False
        
        try:
            patient = appointment.patient
            appointment_time = appointment.appointment_date.strftime("%d/%m/%Y às %H:%M")
            
            if reminder_type == "24h":
                message = (
                    f"🔔 Lembrete de Consulta\n\n"
                    f"Olá! Você tem uma consulta agendada para:\n"
                    f"📅 {appointment_time}\n\n"
                    f"Por favor, confirme sua presença respondendo 'sim' ou 'não'.\n"
                    f"Se precisar remarcar, é só me avisar!"
                )
            else:  # 2h
                message = (
                    f"⏰ Consulta em 2 horas!\n\n"
                    f"Sua consulta está marcada para:\n"
                    f"📅 {appointment_time}\n\n"
                    f"Nos vemos em breve! 🏥"
                )
            
            success = self.whatsapp_service.send_message(patient.phone_number, message)
            
            if success:
                # Log the interaction
                interaction = Interaction(
                    patient_id=patient.id,
                    conversation_id=None,  # System message
                    type=InteractionType.OUTGOING,
                    message_text=message,
                    message_type="text"
                )
                self.db.add(interaction)
                self.db.commit()
            
            return success
            
        except Exception as e:
            print(f"Error sending reminder: {e}")
            return False
    
    def _send_reengagement_message(self, appointment: Appointment) -> bool:
        """Send re-engagement message for no-show"""
        if not self.whatsapp_service:
            return False
        
        try:
            patient = appointment.patient
            appointment_time = appointment.appointment_date.strftime("%d/%m/%Y às %H:%M")
            
            message = (
                f"😔 Perdemos você na consulta de {appointment_time}\n\n"
                f"Esperamos que esteja tudo bem! Se precisar reagendar ou "
                f"tiver alguma emergência, estamos aqui para ajudar.\n\n"
                f"Para reagendar, responda 'reagendar' ou entre em contato conosco."
            )
            
            success = self.whatsapp_service.send_message(patient.phone_number, message)
            
            if success:
                # Log the interaction
                interaction = Interaction(
                    patient_id=patient.id,
                    conversation_id=None,  # System message
                    type=InteractionType.OUTGOING,
                    message_text=message,
                    message_type="text"
                )
                self.db.add(interaction)
                self.db.commit()
            
            return success
            
        except Exception as e:
            print(f"Error sending re-engagement message: {e}")
            return False
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get reminder and no-show metrics"""
        try:
            from datetime import timedelta
            from sqlalchemy import func
            
            # Last 30 days metrics
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            # Total appointments
            total_appointments = self.db.query(Appointment).filter(
                Appointment.appointment_date >= thirty_days_ago
            ).count()
            
            # No-shows
            no_shows = self.db.query(Appointment).filter(
                Appointment.status == AppointmentStatus.NO_SHOW,
                Appointment.appointment_date >= thirty_days_ago
            ).count()
            
            # Completed appointments
            completed = self.db.query(Appointment).filter(
                Appointment.status == AppointmentStatus.COMPLETED,
                Appointment.appointment_date >= thirty_days_ago
            ).count()
            
            # Reminder interactions (system messages)
            reminder_interactions = self.db.query(Interaction).filter(
                Interaction.patient_id.isnot(None),
                Interaction.conversation_id.is_(None),
                Interaction.type == InteractionType.OUTGOING,
                Interaction.created_at >= thirty_days_ago
            ).count()
            
            # Calculate rates
            no_show_rate = (no_shows / total_appointments * 100) if total_appointments > 0 else 0
            completion_rate = (completed / total_appointments * 100) if total_appointments > 0 else 0
            
            return {
                "period": "last_30_days",
                "total_appointments": total_appointments,
                "no_shows": no_shows,
                "completed": completed,
                "reminder_messages_sent": reminder_interactions,
                "no_show_rate": round(no_show_rate, 2),
                "completion_rate": round(completion_rate, 2),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def close(self):
        """Close database connection"""
        self.db.close()
