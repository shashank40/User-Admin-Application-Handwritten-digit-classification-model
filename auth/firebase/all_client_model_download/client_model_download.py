import os

import pyrebase

async def downloadClientModels():
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