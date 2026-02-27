import requests
import sys
from config import config

SERVER_URL = config.get_string('server', 'url', 'http://localhost:5000')

def authenticate():
    while True:
        code = input("Enter your test code: ").strip().upper()
        if not code:
            print("Code cannot be empty.")
            continue
        if not code.isalnum():
            print("Code must be alphanumeric.")
            continue
        if len(code) != 8:
            print("Code must be 8 characters.")
            continue

        try:
            response = requests.post(f"{SERVER_URL}/claim_code", json={'code': code})
            data = response.json()
            if response.status_code == 200 and data.get('success'):
                print("Authentication successful.")
                return code
            else:
                print(f"Error: {data.get('message', f'Server error: {response.status_code}')}")
        except requests.RequestException as e:
            print(f"Connection error: {e}")
            sys.exit(1)
        except ValueError:
            print(f"Invalid server response: {response.status_code}")
            sys.exit(1)