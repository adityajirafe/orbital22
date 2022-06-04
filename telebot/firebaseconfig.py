import pyrebase
from dotenv import load_dotenv
import os

load_dotenv()

APIKEY = os.getenv('apiKey')
AUTH_DOMAIN = os.getenv('authDomain')
PROJECT_ID = os.getenv('projectId')
STORAGE_BUCKET = os.getenv('storageBucket')
MESSAGING_SENDER_ID = os.getenv('messagingSenderId')
APP_ID = os.getenv('appId')
MEASUREMENT_ID = os.getenv('measurementId')
DATABASE_URL = os.getenv('databaseURL')

firebaseConfig = {
    "apiKey" : APIKEY,
    "authDomain" : AUTH_DOMAIN,
    "projectId" : PROJECT_ID,
    "storageBucket" : STORAGE_BUCKET,
    "messagingSenderId" : MESSAGING_SENDER_ID,
    "appId" : APP_ID,
    "measurementId" : MEASUREMENT_ID,
    'databaseURL' : DATABASE_URL
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# data = {'name': 'john'}

# db.push(data)

# data = {"Adi": 378, "CY": 331}
# db.child("Users").set(data)

auth = firebase.auth()

# def signup():
#     email = input("Enter your email: ")
#     password = input("Enter your password: ")
    
#     user = auth.create_user_with_email_and_password(email, password)
#     print('success')

def login(email, password, authen):
    try: 
      print(f"Logging in {email}")
      authen.sign_in_with_email_and_password(email, password)
      return True
    except:
      print(f"User {email} not found")
      return False

# signup()

# db.child("Users").child("Adi").update({'Age': 22})

# result = db.order_by_key().limit_to_last(3).get()
# print(result.val())