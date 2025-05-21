from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("MS_CLIENT_ID")
client_secret = os.getenv("MS_CLIENT_SECRET")
tenant_id = os.getenv("MS_TENANT_ID")

authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]

app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority
)

print("🔐 Requesting token...")

result = app.acquire_token_for_client(scopes=scope)

if "access_token" in result:
    print("✅ Access token received")
    print(result["access_token"][:60] + "...")
else:
    print("❌ Token request failed")
    print("🛑 Error:", result.get("error"))
    print("📝 Description:", result.get("error_description"))
    print("🔗 Correlation ID:", result.get("correlation_id"))