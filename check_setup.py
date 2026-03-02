import os
from dotenv import load_dotenv

# This line looks for the .env file and loads it
load_dotenv()

# This line tries to grab the URL you just pasted
db_url = os.getenv("DATABASE_URL")

if db_url:
    print("✅ Success! Your .env file is set up correctly.")
    print(f"Connection string found for host: {db_url.split('@')[1].split('/')[0]}")
else:
    print("❌ Error: I can't find the DATABASE_URL. Check your .env file name!")