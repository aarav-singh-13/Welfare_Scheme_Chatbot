# Welfare Scheme Chatbot

A multilingual, AI-powered WhatsApp conversational assistant designed to bridge the information asymmetry gap for Indian rural citizens. Built for the AI & Intelligent Solutions Track.

## 🚀 Overview

Despite over 950 welfare schemes existing in India, fewer than 40% of eligible rural beneficiaries claim them due to language barriers and complex documentation. 

This project solves the "last-mile discovery" problem using a WhatsApp bot powered by **Google's Gemini 2.5 Flash** and a strict **RAG (Retrieval-Augmented Generation)** architecture to completely eliminate AI hallucinations regarding government policy.

## 🛠️ Tech Stack
*   **Backend:** Python, FastAPI, Uvicorn
*   **AI Engine:** Google Gemini 2.5 Flash (via `google-generativeai`)
*   **Integration:** Twilio WhatsApp Business API
*   **Environment Setup:** `python-dotenv`

## ⚙️ How to Run Locally

### 1. Install Dependencies
Ensure you have Python installed, then install the required packages:
```bash
pip install fastapi uvicorn google-generativeai twilio pydantic python-multipart python-dotenv
```

### 2. Setup Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
GEMINI_API_KEY=your_google_ai_studio_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

### 3. Start the Backend Server
Run the FastAPI application:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Expose the Server (ngrok)
To allow Twilio to reach your local server, open a new terminal and run ngrok:
```bash
ngrok http 8000
```
*Copy the `https://xxxx.ngrok-free.app` URL.*

### 5. Configure Twilio Sandbox
1. Go to your Twilio Console -> Messaging -> Try it out -> Send a WhatsApp message.
2. Under "Sandbox settings", paste your ngrok URL into the "WHEN A MESSAGE COMES IN" field and add `/twilio/webhook` to the end.
   *(Example: `https://xxxx.ngrok-free.app/twilio/webhook`)*
3. Save the settings.

## 📱 Testing the Bot

To initiate a conversation with the Twilio sandbox from your personal WhatsApp:

1. **Join the Sandbox:** You must first send the exact phrase **`join onto-driven`** to the Twilio Sandbox phone number.
2. **Start Chatting:** Once connected, send a greeting in Hindi, English, or Hinglish! 

**Example Test Persona:**
> "Main kisan hu, meri umar 45 saal hai aur mere paas zameen hai."

The AI will parse your demographic data against the `schemes_db.json` database and instantly reply with PM-KISAN & Ayushman Bharat eligibility and document checklists.
