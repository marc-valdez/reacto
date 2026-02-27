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

    supabase.rpc("create_participant_if_not_exists").execute()

    return supabase, session
