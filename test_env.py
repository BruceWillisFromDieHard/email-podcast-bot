from dotenv import load_dotenv, find_dotenv
import os

env_path = find_dotenv()
print("✅ .env path found at:", env_path)

load_dotenv(env_path)
print("🔍 MS_TENANT_ID =", os.getenv("MS_TENANT_ID"))