import time
from typing import Dict, Any, List

class StateManager:
    def __init__(self):
        # In-memory session store. Key: phone_number, Value: session data
        self.sessions: Dict[str, Dict[str, Any]] = {}
        # Session timeout in seconds (e.g., 30 mins)
        self.session_timeout = 1800

    def get_session(self, phone_number: str) -> Dict[str, Any]:
        """Retrieve a session or create a new one if it doesn't exist or expired."""
        current_time = time.time()
        
        if phone_number in self.sessions:
            session = self.sessions[phone_number]
            # Check if session expired
            if current_time - session.get('last_activity', 0) > self.session_timeout:
                self.clear_session(phone_number)
            else:
                # Update last activity
                session['last_activity'] = current_time
                return session

        # Create new session
        new_session = {
            'phone_number': phone_number,
            'history': [], # Store previous turns for context
            'last_activity': current_time,
            'question_count': 0 # To track progress through the 4-6 questions
        }
        self.sessions[phone_number] = new_session
        return new_session

    def update_session(self, phone_number: str, user_message: str, bot_reply: str):
        """Update session history and metadata."""
        session = self.get_session(phone_number)
        session['history'].append({"role": "user", "parts": [user_message]})
        session['history'].append({"role": "model", "parts": [bot_reply]})
        session['question_count'] += 1
        session['last_activity'] = time.time()
        self.sessions[phone_number] = session

    def clear_session(self, phone_number: str):
        """Clear a user's session."""
        if phone_number in self.sessions:
            del self.sessions[phone_number]

state_manager = StateManager()
