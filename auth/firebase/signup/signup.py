# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import auth

# def signupAuth(email: str, password: str):
#     # Use a service account.
#     cred = credentials.Certificate('auth/firebase/secret/dsci2023-firebase-adminsdk-t47pf-555db158e8.json')

#     if not firebase_admin._apps:
#         app = firebase_admin.initialize_app(cred)
#     try:
#         user = auth.create_user(email=email, password=password)
#         return True
#     except Exception as e:
#        return False

import json
# import os
import requests

FIREBASE_WEB_API_KEY = 'AIzaSyBMavTENGI2KJvlQRhrz9wzrvB-G4gVZ_0' 
# os.environ.get("FIREBASE_WEB_API_KEY")
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp"

def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
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
            return 'Sucessfully Signed Up', True
    except Exception as e:
        return 'Error in Signing Up' + e, False

