import os
from supabase import create_client
from config import config

session_file = "supabase_session.json"

def authenticate():
    supabase = create_client(
        config.get_string("auth", "SUPABASE_URL"),
        config.get_string("auth", "SUPABASE_KEY")
    )

    email = input("Enter your email: ")
    supabase.auth.sign_in_with_otp({"email": email})
    otp = input("Enter the code sent to your email: ")
    session = supabase.auth.verify_otp({
        "email": email,
        "token": otp,
        "type": "email"
    })

    print(f"Logged in as {email}.")

    try:
        supabase.rpc("init_participant_or_block").execute()
    except Exception:
        print("You have already completed this test.")
        supabase.auth.sign_out()
        exit()

    return supabase, session
