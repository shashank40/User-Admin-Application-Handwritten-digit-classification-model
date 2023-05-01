
import firebase_admin
from firebase_admin import credentials, storage


async def baseUpload():
    cred = credentials.Certificate('auth/firebase/secret/dsci2023-firebase-adminsdk-t47pf-555db158e8.json')

    app = firebase_admin.initialize_app(cred, {'storageBucket': 'dsci2023.appspot.com'})

    # Put your local file path 
    fileName = "saved_model/final_model.h5"
    bucket = storage.bucket()
    blob = bucket.blob('base_model/final_model.h5')
    blob.upload_from_filename(fileName)

    # Opt : if you want to make public access from the URL
    blob.make_public()

    # gives public url
    # print("your file url", blob.public_url)