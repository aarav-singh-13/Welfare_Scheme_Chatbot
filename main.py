from fastapi import FastAPI
import uvicorn
from routes import twilio_webhook

app = FastAPI(
    title="Welfare Scheme Chatbot API",
    description="Backend for the Multilingual WhatsApp Chatbot for Indian Welfare Schemes.",
    version="1.0.0"
)

# Include the Twilio router
app.include_router(twilio_webhook.router, prefix="/twilio", tags=["Twilio"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welfare Scheme Chatbot API is running. Point your Twilio webhook to /twilio/webhook"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
