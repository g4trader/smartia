import os, hmac, hashlib, json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SmartIA API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

# Meta WhatsApp verification (GET) + webhook (POST)
VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "dev-token")

@app.get("/webhook/whatsapp", response_class=PlainTextResponse)
async def verify(mode: str = "", challenge: str = "", verify_token: str = ""):
    # Meta sends: hub.mode, hub.challenge, hub.verify_token
    # We accept both snake and original for convenience
    token = verify_token or ""
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook/whatsapp")
async def receive_webhook(request: Request):
    body = await request.json()
    # TODO: normalize payload across providers (Meta/Twilio/Zenvia)
    # Route to orchestrator
    print("Incoming webhook:", json.dumps(body)[:2000])
    # Example: echo message or trigger scheduling flow
    return JSONResponse({"received": True})

# Example protected endpoint for scheduling (stub)
@app.post("/schedule")
async def schedule(payload: dict):
    # TODO: integrate with Google Calendar/Notion/CRM
    return {"ok": True, "payload": payload}
