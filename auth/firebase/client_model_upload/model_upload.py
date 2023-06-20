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
            "apiKey": "XXXXX",
            "authDomain": "XXXX.firebaseapp.com",
            "databaseURL": "XXXX",
            "projectId": "XXXX",
            "storageBucket": "XXXX.appspot.com",
            "serviceAccount": "auth/firebase/secret/XXXX.json",
            }

            firebase_storage = pyrebase.initialize_app(config)

            storage = firebase_storage.storage()

            file_name = email.replace('.','_')

            storage.child(f'client_model/{file_name}.h5').put(file.file)
            return 'Upload Successful', True

        except Exception as e:
            print(e)
            return f'Error in Uploading Model : {e}', False
