import os
import pyrebase
from dotenv import load_dotenv


load_dotenv()

"""Retrieve details from env"""
APIKEY = os.getenv('apiKey')
AUTH_DOMAIN = os.getenv('authDomain')
PROJECT_ID = os.getenv('projectId')
STORAGE_BUCKET = os.getenv('storageBucket')
MESSAGING_SENDER_ID = os.getenv('messagingSenderId')
APP_ID = os.getenv('appId')
MEASUREMENT_ID = os.getenv('measurementId')
DATABASE_URL = os.getenv('databaseURL')


"""Initialise firebase config"""
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

auth = firebase.auth()


"""Authenticate users"""
def login(email, password, authen):
    try: 
      print(f"Logging in {email}")
      authen.sign_in_with_email_and_password(email, password)
      return True
    except:
      print(f"User {email} not found")
      return False