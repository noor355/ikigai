import sys
import os
import requests

def test_api_endpoints():
    base_url = "http://localhost:8000/api/v1"
    
    print("Checking API router configuration...")
    
    # Check if /api/v1/daily-entries/ exists
    try:
        # We expect a 401 if it exists but we're not auth'd, or 200/404/etc
        response = requests.get(f"{base_url}/daily-entries/")
        print(f"GET /daily-entries/: {response.status_code}")
    except Exception as e:
        print(f"Error connecting to /daily-entries/: {e}")

    try:
        response = requests.post(f"{base_url}/recommendations/save-daily-entry")
        print(f"POST /recommendations/save-daily-entry: {response.status_code}")
    except Exception as e:
        print(f"Error connecting to /recommendations/save-daily-entry: {e}")

if __name__ == "__main__":
    test_api_endpoints()
