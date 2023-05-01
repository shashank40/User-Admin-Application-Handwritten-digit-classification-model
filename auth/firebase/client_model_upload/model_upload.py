import pyrebase
from fastapi import UploadFile


from auth.firebase.user_exists.user_exists import account_exists

async def uploadClientModel(email: str, idToken: str, file: UploadFile):

    message, status = await account_exists(idToken, email)

    if status == False:
        print(message)
        return message, False
    else:
        try :
            config = {
            "apiKey": "AIzaSyBMavTENGI2KJvlQRhrz9wzrvB-G4gVZ_0",
            "authDomain": "dsci2023.firebaseapp.com",
            "databaseURL": "https://dsci2023.firebaseio.com",
            "projectId": "dsci2023",
            "storageBucket": "dsci2023.appspot.com",
            "serviceAccount": "auth/firebase/secret/client-service.json",
            }

            firebase_storage = pyrebase.initialize_app(config)

            storage = firebase_storage.storage()

            storage.child(f'client_model/{email}.h5').put(file.file)
            return 'Upload Successful', True

        except Exception as e:
            print(e)
            return f'Error in Uploading Model : {e}', False
