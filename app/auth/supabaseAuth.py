from supabase import create_client, Client
from ..helper import Helper

url = Helper().getEnv("SUPABASE_URL")
key = Helper().getEnv("SUPABASE_KEY")
supabaseClient: Client = create_client(url, key)