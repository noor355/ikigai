import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from routes_chat_new import ChatMessageCreate
import asyncio
from unittest.mock import MagicMock
import datetime

async def test_chat_logic():
    print("Testing Chat Logic Improvements...")
    
    # Mock user with profile
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_user.full_name = "Test User"
    mock_user.profile = MagicMock()
    mock_user.profile.interests = ["technology", "coding"]
    mock_user.profile.skills = ["Python"]
    
    # Mock database
    mock_db = MagicMock()
    mock_db.query().filter().order_by().limit().all.return_value = []
    
    # Test cases
    test_cases = [
        ("hi", "I've been thinking about your journey."),
        ("tell me about ikigai", "Which of these four areas feels like your strongest foundation right now"),
        ("give me a recommendation", "what's one skill you're proud of, even if it's not on your resume yet?"),
    ]
    
    from routes_chat_new import chat_with_coach
    
    for message, expected_part in test_cases:
        chat_input = ChatMessageCreate(message=message)
        response = await chat_with_coach(chat_input, current_user=mock_user, db=mock_db)
        
        reply = response.reply
        print(f"User: {message}")
        print(f"Coach: {reply}")
        
        if expected_part in reply:
            print(f"✅ PASS: Found expected content: {expected_part}")
        else:
            print(f"❌ FAIL: Expected to find '{expected_part}' in '{reply}'")
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(test_chat_logic())
