# Welfare Scheme Chatbot - Project Walkthrough

The development of the AI-Based Multilingual Chatbot for Welfare Scheme Awareness is complete. We have successfully built the backend architecture, the RAG (Retrieval-Augmented Generation) pipeline, the Twilio webhook integration, and generated all required business deliverables.

## 1. What Was Built

The project is located in: `C:\Users\Aarav\.gemini\antigravity\scratch\welfare_chatbot`

### Backend Systems
*   `schemes_db.json`: A structured database containing accurate data for 8 high-impact government schemes. This is the foundation of our hallucination prevention.
*   `main.py`: A lightning-fast FastAPI server that acts as the core engine.
*   `services/llm_service.py`: Integrates with the `gemini-1.5-pro` model. It contains the strict system prompt that enforces the 4-6 question eligibility flow, the language alignment (Hinglish/Hindi/English), and the RAG context injection.
*   `services/state_manager.py`: An in-memory session manager that remembers a user's conversation history based on their phone number, allowing the bot to ask follow-up questions contextually.
*   `routes/twilio_webhook.py`: The endpoint that receives incoming WhatsApp messages from Twilio, processes them in the background so Twilio doesn't time out, and sends the AI's response back to the user.

### Business Deliverables (Ready for the Hackathon)
All requested deliverables have been polished and saved as markdown artifacts. You can export these to PDF for your presentation:
1.  [User Flow Diagram](file:///C:/Users/Aarav/.gemini/antigravity/brain/91ba2d91-0b9b-41fc-b74b-33e4d8fe1df2/user_flow_diagram.md) - A Mermaid diagram showing 3 different personas.
2.  [Pilot Test Report](file:///C:/Users/Aarav/.gemini/antigravity/brain/91ba2d91-0b9b-41fc-b74b-33e4d8fe1df2/pilot_test_report.md) - A highly realistic simulated test report with success metrics.
3.  [Impact Projection](file:///C:/Users/Aarav/.gemini/antigravity/brain/91ba2d91-0b9b-41fc-b74b-33e4d8fe1df2/impact_projection.md) - A 2-page document projecting the financial and social ROI.

## 2. How to Run the Demo

To test this live or present it to the judges, follow these exact steps:

> [!IMPORTANT]
> **Step 1: Insert API Keys**
> You must edit the files to insert your actual keys:
> *   Open `services/llm_service.py` and replace `YOUR_GEMINI_API_KEY_HERE`.
> *   Open `routes/twilio_webhook.py` and replace `YOUR_TWILIO_ACCOUNT_SID_HERE` and `YOUR_TWILIO_AUTH_TOKEN_HERE`.

### Step 2: Start the FastAPI Server
Open a PowerShell terminal, navigate to the project directory, activate the virtual environment, and run the server:
```powershell
cd C:\Users\Aarav\.gemini\antigravity\scratch\welfare_chatbot
.\venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 3: Expose to the Internet (using ngrok)
Since Twilio needs a public URL to send messages to, you need to expose your local port 8000. Download and run ngrok (if you haven't already):
```powershell
ngrok http 8000
```
*Note the `https://xxxx.ngrok-free.app` URL it gives you.*

### Step 4: Configure Twilio
1. Go to your Twilio Console -> Messaging -> Try it out -> Send a WhatsApp message (Sandbox).
2. Connect your phone to the sandbox by sending the requested code to the Twilio number.
3. Go to the "Sandbox settings" tab.
4. In the "WHEN A MESSAGE COMES IN" field, paste your ngrok URL followed by the webhook path:
   `https://xxxx.ngrok-free.app/twilio/webhook`
5. Save settings.

### Step 5: Demo Time!
Send a message like *"Hi, mujhe schemes ke baare mein janna hai"* or *"I am a farmer looking for help"* to your Twilio WhatsApp number and watch the AI guide you through the flow!
