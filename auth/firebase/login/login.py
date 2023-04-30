import json
# import os
import requests

FIREBASE_WEB_API_KEY = 'AIzaSyBMavTENGI2KJvlQRhrz9wzrvB-G4gVZ_0' 
# os.environ.get("FIREBASE_WEB_API_KEY")
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

def log_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })
    try:
        r = requests.post(rest_api_url,
                        params={"key": FIREBASE_WEB_API_KEY},
                        data=payload)
        if 'error' in r.json().keys():
            return r.json()['error']['message'], False
        else:
            return 'Sucessfully Logged In', True
    except Exception as e:
        return 'Error in Logging Up' + e, False