import sys
import os

# Add the project directory to path so we can import services
sys.path.append(r"C:\Users\Aarav\Downloads\Welfare_Chatbot_Project")

from services.llm_service import model, SCHEMES_DATA

try:
    print("Testing Gemini API Generation...")
    chat = model.start_chat(history=[])
    response = chat.send_message("Main kisan hu, meri umar 45 saal hai aur mere paas zameen hai.")
    print("Response Text:\n", response.text)
    print("Finish Reason:", response.candidates[0].finish_reason)
except Exception as e:
    import traceback
    traceback.print_exc()
