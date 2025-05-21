from dotenv import load_dotenv
import os

load_dotenv()
print("MS_TENANT_ID:", os.getenv("MS_TENANT_ID"))