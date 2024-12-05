from supabase import create_client, Client

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9idmJra2F2bWV4em16ZW9maXluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMzNzI5MjgsImV4cCI6MjA0ODk0ODkyOH0.pPkteDjg_jUsb6vgiWLjBl8AKE08UzSiIa9gsFvkLhk"
URL = "https://obvbkkavmexzmzeofiyn.supabase.co"

try:
    supabase: Client = create_client(
        supabase_key=API_KEY,
        supabase_url=URL,
    )
    
    print("Supabase client succesfully initilized")

except Exception as e:
    print(f"Error initializing Supabase client: {e}")


