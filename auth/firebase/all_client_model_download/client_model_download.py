import os

import pyrebase

async def downloadClientModels():
    try :
        config = {
        "apiKey": "AIzaSyBMavTENGI2KJvlQRhrz9wzrvB-G4gVZ_0",
        "authDomain": "dsci2023.firebaseapp.com",
        "databaseURL": "https://dsci2023.firebaseio.com",
        "projectId": "dsci2023",
        "storageBucket": "dsci2023.appspot.com",
        "serviceAccount": "auth/firebase/secret/dsci2023-firebase-adminsdk-t47pf-555db158e8.json",
        }

        firebase_storage = pyrebase.initialize_app(config)

        storage = firebase_storage.storage()

        all_files = storage.list_files()
        all_files = [file for file in all_files if 'client_model' in file.name]
        print(all_files)
        for file in all_files:
            file_name = file.name.split('/')[1]
            if len(file_name):
                file.download_to_filename('temp_models/'+file.name.split('/')[1])

        return 'Download Successful', True

    except Exception as e:
        print(e)
        return f'Error in Downloading Client Models : {e}', False


async def cleanFolder():
    path = 'temp_models/'
    os.system('rm -rf %s/*' % path)