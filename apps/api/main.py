import os, hmac, hashlib, json
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import PlainTextResponse, JSONResponse
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from models import engine, Base, Patient, Interaction, Appointment, AppointmentStatus
from models.database import get_db
from providers.factory import ProviderFactory
from orchestrator import FlowOrchestrator, WhatsAppService
from services import GoogleCalendarService
from jobs import ReminderJob

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartIA API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/providers")
def get_available_providers():
    """Get list of available WhatsApp providers"""
    available = ProviderFactory.get_available_providers()
    return {
        "available_providers": available,
        "default_provider": available[0] if available else None
    }

# Generic webhook endpoints for multiple providers
@app.get("/webhook/{provider}", response_class=PlainTextResponse)
async def verify_webhook(
    provider: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Verify webhook for any provider"""
    try:
        provider_instance = ProviderFactory.create_provider(provider)
        
        # Get query parameters
        query_params = dict(request.query_params)
        
        if provider_instance.verify_webhook(query_params):
            # Return challenge for Meta, or success for others
            if provider == "meta":
                return query_params.get("hub.challenge", "")
            else:
                return "OK"
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/{provider}")
async def receive_webhook(
    provider: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Receive webhook from any provider"""
    try:
        # Create provider instance
        provider_instance = ProviderFactory.create_provider(provider)
        
        # Parse request body based on provider
        if provider == "meta":
            body = await request.json()
        else:
            # For Twilio and others, parse form data
            form_data = await request.form()
            body = dict(form_data)
        
        # Parse webhook payload
        parsed_messages = provider_instance.parse_webhook(body)
        
        # Initialize services
        whatsapp_service = WhatsAppService(provider=provider.upper())
        
        # Initialize calendar service (optional)
        calendar_service = None
        try:
            calendar_service = GoogleCalendarService()
        except Exception as e:
            print(f"Calendar service not available: {e}")
        
        orchestrator = FlowOrchestrator(db, whatsapp_service, calendar_service)
        
        # Process each message
        for parsed_message in parsed_messages:
            success = orchestrator.process_message(parsed_message)
            if not success:
                print(f"Failed to process message: {parsed_message.message_id}")
        
        print(f"Processed {len(parsed_messages)} messages from {provider} webhook")
        return JSONResponse({"received": True, "processed": len(parsed_messages), "provider": provider})
        
    except ValueError as e:
        return JSONResponse({"received": False, "error": str(e)}, status_code=400)
    except Exception as e:
        print(f"Error processing {provider} webhook: {e}")
        return JSONResponse({"received": False, "error": str(e)}, status_code=500)

# Legacy endpoint for backward compatibility
@app.get("/webhook/whatsapp", response_class=PlainTextResponse)
async def verify_legacy(mode: str = "", challenge: str = "", verify_token: str = ""):
    """Legacy Meta webhook verification endpoint"""
    return await verify_webhook("meta", type('Request', (), {'query_params': type('Params', (), {
        'hub.mode': mode,
        'hub.challenge': challenge,
        'hub.verify_token': verify_token
    })()})())

@app.post("/webhook/whatsapp")
async def receive_webhook_legacy(request: Request, db: Session = Depends(get_db)):
    """Legacy webhook endpoint - defaults to Meta provider"""
    return await receive_webhook("meta", request, db)

# Calendar endpoints
@app.get("/calendar/slots")
async def get_available_slots(
    start_date: str,
    end_date: str,
    duration_minutes: int = 60,
    db: Session = Depends(get_db)
):
    """Get available time slots from calendar"""
    try:
        from datetime import datetime
        from services import GoogleCalendarService
        
        # Parse dates
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        # Initialize calendar service
        calendar_service = GoogleCalendarService()
        slots = calendar_service.list_slots(start, end, duration_minutes)
        
        # Filter only available slots
        available_slots = [slot for slot in slots if slot.available]
        
        return {
            "available_slots": [
                {
                    "start": slot.start.isoformat(),
                    "end": slot.end.isoformat()
                }
                for slot in available_slots
            ]
        }
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/calendar/events/{event_id}")
async def get_event(event_id: str, db: Session = Depends(get_db)):
    """Get event details by ID"""
    try:
        from services import GoogleCalendarService
        
        calendar_service = GoogleCalendarService()
        event = calendar_service.get_event(event_id)
        
        if event:
            return {
                "id": event.id,
                "title": event.title,
                "start": event.start.isoformat(),
                "end": event.end.isoformat(),
                "description": event.description,
                "attendees": event.attendees
            }
        else:
            return JSONResponse({"error": "Event not found"}, status_code=404)
            
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.delete("/calendar/events/{event_id}")
async def cancel_event(event_id: str, db: Session = Depends(get_db)):
    """Cancel an event"""
    try:
        from services import GoogleCalendarService
        
        calendar_service = GoogleCalendarService()
        success = calendar_service.cancel_event(event_id)
        
        if success:
            return {"message": "Event cancelled successfully"}
        else:
            return JSONResponse({"error": "Failed to cancel event"}, status_code=500)
            
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# CRM Endpoints
@app.get("/patients")
async def get_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of patients"""
    patients = db.query(Patient).offset(skip).limit(limit).all()
    
    return {
        "patients": [
            {
                "id": patient.id,
                "phone_number": patient.phone_number,
                "name": patient.name,
                "email": patient.email,
                "created_at": patient.created_at.isoformat() if patient.created_at else None,
                "appointments_count": len(patient.appointments)
            }
            for patient in patients
        ]
    }

@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get patient details by ID"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        return JSONResponse({"error": "Patient not found"}, status_code=404)
    
    return {
        "id": patient.id,
        "phone_number": patient.phone_number,
        "name": patient.name,
        "email": patient.email,
        "created_at": patient.created_at.isoformat() if patient.created_at else None,
        "notes": patient.notes,
        "appointments": [
            {
                "id": apt.id,
                "title": apt.title,
                "appointment_date": apt.appointment_date.isoformat(),
                "status": apt.status.value,
                "duration_minutes": apt.duration_minutes
            }
            for apt in patient.appointments
        ],
        "conversations_count": len(patient.conversations),
        "interactions_count": len(patient.interactions)
    }

@app.get("/appointments")
async def get_appointments(
    from_date: str = None,
    to_date: str = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get appointments with optional filters"""
    query = db.query(Appointment)
    
    # Apply filters
    if from_date:
        from datetime import datetime
        start_date = datetime.fromisoformat(from_date)
        query = query.filter(Appointment.appointment_date >= start_date)
    
    if to_date:
        from datetime import datetime
        end_date = datetime.fromisoformat(to_date)
        query = query.filter(Appointment.appointment_date <= end_date)
    
    if status:
        try:
            status_enum = AppointmentStatus(status)
            query = query.filter(Appointment.status == status_enum)
        except ValueError:
            return JSONResponse({"error": "Invalid status"}, status_code=400)
    
    appointments = query.offset(skip).limit(limit).all()
    
    return {
        "appointments": [
            {
                "id": apt.id,
                "patient_id": apt.patient_id,
                "patient_name": apt.patient.name if apt.patient else None,
                "patient_phone": apt.patient.phone_number if apt.patient else None,
                "title": apt.title,
                "appointment_date": apt.appointment_date.isoformat(),
                "duration_minutes": apt.duration_minutes,
                "status": apt.status.value,
                "calendar_event_id": apt.calendar_event_id,
                "created_at": apt.created_at.isoformat() if apt.created_at else None
            }
            for apt in appointments
        ]
    }

@app.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """Get clinic metrics"""
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # Total patients
    total_patients = db.query(Patient).count()
    
    # Total appointments
    total_appointments = db.query(Appointment).count()
    
    # Appointments by status
    appointments_by_status = db.query(
        Appointment.status,
        func.count(Appointment.id)
    ).group_by(Appointment.status).all()
    
    # No-shows (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    no_shows = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.NO_SHOW,
        Appointment.appointment_date >= thirty_days_ago
    ).count()
    
    # Completed appointments (last 30 days)
    completed = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.COMPLETED,
        Appointment.appointment_date >= thirty_days_ago
    ).count()
    
    # Confirmation rate
    total_scheduled = db.query(Appointment).filter(
        Appointment.appointment_date >= thirty_days_ago
    ).count()
    
    confirmation_rate = (completed / total_scheduled * 100) if total_scheduled > 0 else 0
    
    # Lead to consultation rate (patients with appointments / total patients)
    patients_with_appointments = db.query(Patient).join(Appointment).distinct().count()
    lead_to_consultation_rate = (patients_with_appointments / total_patients * 100) if total_patients > 0 else 0
    
    return {
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "appointments_by_status": {
            status.value: count for status, count in appointments_by_status
        },
        "last_30_days": {
            "no_shows": no_shows,
            "completed": completed,
            "confirmation_rate": round(confirmation_rate, 2),
            "lead_to_consultation_rate": round(lead_to_consultation_rate, 2)
        }
    }

# Job endpoints
@app.post("/jobs/reminders/24h")
async def run_24h_reminders(db: Session = Depends(get_db)):
    """Run 24-hour reminder job"""
    try:
        job = ReminderJob()
        result = job.send_reminders_24h()
        job.close()
        return result
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/jobs/reminders/2h")
async def run_2h_reminders(db: Session = Depends(get_db)):
    """Run 2-hour reminder job"""
    try:
        job = ReminderJob()
        result = job.send_reminders_2h()
        job.close()
        return result
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/jobs/no-shows")
async def run_no_show_handler(db: Session = Depends(get_db)):
    """Run no-show handler job"""
    try:
        job = ReminderJob()
        result = job.handle_no_shows()
        job.close()
        return result
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/jobs/metrics")
async def get_job_metrics(db: Session = Depends(get_db)):
    """Get reminder and no-show metrics"""
    try:
        job = ReminderJob()
        result = job.get_metrics()
        job.close()
        return result
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
