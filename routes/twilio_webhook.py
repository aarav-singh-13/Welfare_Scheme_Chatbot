import os
from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

from services.llm_service import generate_response
from services.state_manager import state_manager

load_dotenv()

router = APIRouter()

# Twilio Account details
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")

def send_whatsapp_message(to_number: str, from_number: str, body: str):
    """Sends a WhatsApp message using Twilio's REST API."""
    if "YOUR_TWILIO_ACCOUNT_SID_HERE" in TWILIO_ACCOUNT_SID:
        print(f"MOCK SEND to {to_number}: {body}")
        return
        
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        print(f"Message sent successfully: {message.sid}")
    except Exception as e:
        print(f"Error sending message: {e}")

async def process_whatsapp_message(sender: str, recipient: str, body: str):
    """Background task to process the message and send the reply."""
    # 1. Retrieve session history
    session = state_manager.get_session(sender)
    history = session['history']
    
    # 2. Call Gemini
    print(f"Calling Gemini for {sender} with message: {body}")
    bot_reply = generate_response(body, history)
    
    # 3. Update session
    state_manager.update_session(sender, body, bot_reply)
    
    # 4. Send reply back to user via Twilio
    send_whatsapp_message(to_number=sender, from_number=recipient, body=bot_reply)

@router.post("/webhook")
async def twilio_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Endpoint that Twilio calls when a WhatsApp message is received.
    We return a 200 OK immediately and process the message in the background.
    """
    form_data = await request.form()
    
    # Extract data from Twilio's webhook payload
    sender = form_data.get("From", "")
    recipient = form_data.get("To", "")
    body = form_data.get("Body", "").strip()
    
    print(f"Received message from {sender}: {body}")
    
    # Add to background tasks so Twilio doesn't timeout waiting for LLM
    background_tasks.add_task(process_whatsapp_message, sender, recipient, body)
    
    # Return empty TwiML response immediately
    return PlainTextResponse(content=str(MessagingResponse()), media_type="application/xml")
