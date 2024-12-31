from supabase import create_client, Client


API_KEY = SUPABASE_KEY

URL = "https://obvbkkavmexzmzeofiyn.supabase.co"

try:
    supabase: Client = create_client(
        supabase_key=API_KEY,
        supabase_url=URL,
    )
    
    print("Supabase client succesfully initilized")

except Exception as e:
    print(f"Error initializing Supabase client: {e}")


