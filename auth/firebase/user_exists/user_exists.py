import json
# import os
import requests

FIREBASE_WEB_API_KEY = 'XXXXXX' 
# os.environ.get("FIREBASE_WEB_API_KEY")
rest_api_url = f"https://identitytoolkit.googleapis.com//v1/accounts:lookup"

async def account_exists(idToken: str, email: str):
    payload = json.dumps({
        "idToken": idToken,
    })
    try:
        r = requests.post(rest_api_url,
                        params={"key": FIREBASE_WEB_API_KEY},
                        data=payload)
        if 'error' in r.json().keys():
            return r.json()['error']['message'], False
        else:
            if r.json()['users'][0]['email'] == email:
                return 'User Exists', True
            else:
                return 'Invalid Email Address. Input Correct Email Address for Uploading Latest Model', False
    except Exception as e:
        return f'Error : {e}', False