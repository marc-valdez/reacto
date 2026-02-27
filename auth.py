import os
import random
import string
import sys
from config import config

AUTH_FILE = config.get_string('auth', 'auth_codes_file', 'auth_codes.txt')
USED_FILE = config.get_string('auth', 'used_codes_file', 'used_codes.txt')

def generate_codes():
    codes = set()
    while len(codes) < 100:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        codes.add(code)
    with open(AUTH_FILE, 'w') as f:
        for code in codes:
            f.write(code + '\n')
    # Create empty used file
    with open(USED_FILE, 'w') as f:
        pass

def load_codes():
    if not os.path.exists(AUTH_FILE):
        generate_codes()
    with open(AUTH_FILE, 'r') as f:
        codes = set(line.strip() for line in f if line.strip())
    return codes

def load_used():
    if not os.path.exists(USED_FILE):
        return set()
    with open(USED_FILE, 'r') as f:
        used = set(line.strip() for line in f if line.strip())
    return used

def save_used(used):
    with open(USED_FILE, 'w') as f:
        for code in used:
            f.write(code + '\n')

def authenticate():
    codes = load_codes()
    used = load_used()
    available = codes - used
    if not available:
        print("No available test codes. Exiting.")
        sys.exit(1)
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
        if code not in codes:
            print("Invalid code.")
            continue
        if code in used:
            print("Code already used.")
            continue
        # Valid
        used.add(code)
        save_used(used)
        print("Authentication successful.")
        return code