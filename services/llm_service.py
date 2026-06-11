import os
import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

# Load Scheme Database
DB_PATH = Path(__file__).parent.parent / "schemes_db.json"
try:
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        SCHEMES_DATA = json.load(f)
except FileNotFoundError:
    SCHEMES_DATA = []

def format_schemes_context(schemes: list) -> str:
    context = "AVAILABLE SCHEMES IN DATABASE:\n"
    for s in schemes:
        context += f"- **{s['scheme_name']}**: {s['description']}\n"
        context += f"  Eligibility: {', '.join(s['eligibility_criteria'])}\n"
        context += f"  Documents Required: {', '.join(s['documents_required'])}\n"
    return context

SYSTEM_PROMPT = f"""
You are an expert, multilingual assistant for Indian Government Welfare Schemes.
Your goal is to help rural citizens discover schemes they are eligible for by asking 4-6 simple questions.

CRITICAL RULES:
1. NO HALLUCINATIONS: You must ONLY recommend schemes listed in the 'AVAILABLE SCHEMES IN DATABASE' section below. If a user asks about a scheme not listed, apologize and say you only have information on the listed schemes.
2. LANGUAGE ALIGNMENT: Detect the language the user speaks (e.g., Hindi, English, Hinglish). Always reply in the user's preferred language. If they use mixed language (Hinglish like "mera aadhaar kho gaya"), reply in simple, clear Hindi written in the Latin alphabet (Hinglish) or Devanagari based on what they use most.
3. ELIGIBILITY FLOW: Your objective is to ask 4-6 questions ONE BY ONE (e.g., age, gender, occupation, land ownership) to determine eligibility. DO NOT ask all questions at once. Keep it conversational.
4. EXTREME CONCISENESS (CRITICAL): You must respond as fast as possible. Keep answers under 20 words unless you are listing the final schemes. Do not use filler words.
5. FINAL OUTPUT: If the user has already provided their core details (e.g., occupation, age, and land/income status), DO NOT ask more questions or wait for more turns. IMMEDIATELY provide a personalized shortlist of eligible schemes and a checklist of required documents.
6. NO ADVICE: You are an information assistant, not a legal or medical advisor.

{format_schemes_context(SCHEMES_DATA)}
"""

generation_config = {
  "temperature": 0.0, # Zero temperature to prevent hallucination
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 800, # Increased to prevent text cutting off
}

safety_settings = [
  {
    "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
    "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
  },
  {
    "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
    "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
  },
  {
    "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
    "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
  },
  {
    "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
  }
]

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # Use the best model as requested by user
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=SYSTEM_PROMPT
)

def generate_response(user_message: str, chat_history: list) -> str:
    """
    Generates a response from Gemini using the chat history for context.
    """
    # If the user hasn't provided a key yet, mock the response so it doesn't crash
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return "[SYSTEM: Please replace YOUR_GEMINI_API_KEY_HERE in services/llm_service.py with your actual API key to use the AI.]"
    
    try:
        # Start a chat session using the history
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "I'm sorry, I am currently experiencing technical difficulties. Please try again later."
