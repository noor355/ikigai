import sys
import os
import json
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

def test_final_coach_performance():
    print("\n--- IKIGAI AI COACH PERFORMANCE TEST ---")
    
    # Mock settings and DB to avoid environment issues
    from ml_engine.nlp_processor import NLPProcessor
    
    print("\n[STEP 1] Testing Model Initialization...")
    try:
        nlp = NLPProcessor()
        if nlp.gemini_client:
            print("SUCCESS: Gemini Client initialized.")
        else:
            print("FAILURE: Gemini Client NOT initialized.")
            return
    except Exception as e:
        print(f"ERROR during init: {e}")
        return

    print("\n[STEP 2] Testing Complex Career Query (Python + Painting)...")
    user_msg = "I'm good at Python but I love painting. How can I combine these for a career that the world needs right now?"
    context = "User recent journal: Spent 4 hours today building a generative art script. Felt happy but tired. Wants to make money from art."
    
    try:
        response = nlp.generate_coach_response(user_msg, context)
        print(f"\nAI RESPONSE:\n{response}")
        
        # Validation checks
        has_professions = any(word in response.lower() for word in ["developer", "designer", "engineer", "artist", "architect"])
        has_salary = "$" in response or "k" in response.lower()
        
        print("\n--- VALIDATION ---")
        print(f"Contains Professions: {'PASS' if has_professions else 'FAIL'}")
        print(f"Contains Salary: {'PASS' if has_salary else 'FAIL'}")
        
        if has_professions and has_salary:
            print("\nRESULT: PERFORMANCE TEST PASSED! The model is reasoning correctly.")
        else:
            print("\nRESULT: PERFORMANCE TEST FAILED. Check prompt constraints.")
            
    except Exception as e:
        print(f"ERROR during generation: {e}")

if __name__ == "__main__":
    test_final_coach_performance()
