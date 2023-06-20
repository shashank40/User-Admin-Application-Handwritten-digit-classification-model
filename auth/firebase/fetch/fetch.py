import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def fetchFromFirebase(collection, document):
    # Use a service account.
    cred = credentials.Certificate('auth/firebase/secret/XXXX.json')

    if not firebase_admin._apps:
        app = firebase_admin.initialize_app(cred)

    db = firestore.client()

    doc_ref = db.collection(u'%s'%(collection)).document(u'%s'%(document))

    doc = doc_ref.get().to_dict()

    return doc

