import sys
import os

# Add the project directory to path so we can import services
sys.path.append(r"C:\Users\Aarav\Downloads\Welfare_Chatbot_Project")

from services.llm_service import genai

try:
    print("Listing models...")
    for m in genai.list_models():
        print(f"Name: {m.name}")
        print(f"Supported generation methods: {m.supported_generation_methods}")
except Exception as e:
    import traceback
    traceback.print_exc()
