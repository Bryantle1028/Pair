import pyrebase
from firebase_admin import db

config = {
  "apiKey": "AIzaSyB7JPNqA9oPYkhMV0C4li47eu3eHWuvPG8",
  "authDomain": "whisk-231323.firebaseapp.com",
  "databaseURL": "https://whisk-231323.firebaseio.com",
  "storageBucket": "whisk-231323.appspot.com",
  "serviceAccount": "/Users/BryantLe/Pair/backend/analyzer/whisk-231323-4fa20fd87916.json"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

#authenticate a user
user = auth.sign_in_with_email_and_password("Bryant.Le@Vanderbilt.edu", "WhiskUser1028")

db = firebase.database()
users_ref = db.child('users')
users_ref.set({
    'Bryant': {
        'date_of_birth': 'October 28, 1997',
        'full_name': 'Bryant Le',
    },
    'Wade': {
        'date_of_birth': 'August 27, 1997',
        'full_name': 'Wade Allyn Rance'
    }
})