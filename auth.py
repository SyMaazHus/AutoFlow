import os
from msal import PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AUTHORITY = os.getenv("AZURE_AUTHORITY", "https://login.microsoftonline.com/common")

SCOPES = [
    "User.Read",
    "Files.ReadWrite",
    "Notes.ReadWrite",
    "Calendars.Read"
]

app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)

def get_access_token() -> str | None:
    if not CLIENT_ID:
        print("[GraphAuth] Error: AZURE_CLIENT_ID missing")
        return None

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]

    result = app.acquire_token_interactive(scopes=SCOPES, port=8400)
    if "access_token" in result:
        return result["access_token"]
    
    return None

if __name__ == "__main__":
    token = get_access_token()