import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import utils.firebase.fetch.fetch as fetch


def pushToFirebase(data, collection, document, objectName):
    # Use a service account.
    cred = credentials.Certificate('auth/firebase/secret/XXXX.json')

    if data is None:
        print("data is None")
        return

    if not firebase_admin._apps:
        app = firebase_admin.initialize_app(cred)

    db = firestore.client()
    db_ref = db.collection(u'%s'%(collection)).document(u'%s'%(document))
    if len(objectName) == 1:
        new_arr = fetch.fetchFromFirebase(collection, document)
        new_arr = new_arr[objectName[0]]
        new_arr.append(data)
        print(new_arr)
        db_ref.set({u'%s'%(objectName[0]): new_arr})
    else:
        for i, obj in enumerate(objectName):
            db_ref.set({u'%s'%(obj): data[i]})