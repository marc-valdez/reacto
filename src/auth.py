from supabase import create_client
from src.config import Config

session_file = "supabase_session.json"


def authenticate(config: Config):
    supabase = create_client(
        config.get_string("auth", "SUPABASE_URL"),
        config.get_string("auth", "SUPABASE_KEY"),
    )

    while True:
        try:
            email = input("Enter your email: ")
            supabase.auth.sign_in_with_otp({"email": email})
            otp = input("Enter the code sent to your email: ")
            session = supabase.auth.verify_otp(
                {"email": email, "token": otp, "type": "email"}
            )
            break
        except Exception as e:
            print(f"Error: {e}. Please try again.")

    print(f"Logged in as {email}.")

    try:
        age = input("Plese enter your age: ")
        supabase.rpc("init_participant", {"age": int(age)}).execute()
    except Exception:
        print("You have already completed this test.")
        supabase.auth.sign_out()
        exit()

    return supabase, session
