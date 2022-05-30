# CoinValet

## How to run application:

Ensure you have ```node```, ```npm``` and ```expo-cli``` installed


Pick a local directory and clone this repository with: 

```git clone https://github.com/adityajirafe/orbital22.git```

Once that is done, run ```npm i``` which will install the relevant dependencies necessary to run the application

Following which, firebase setup is required. You can either choose to: 

a) Email us at ```adityajirafe@u.nus.edu``` or ```e0725272@u.nus.edu``` to obtain the Firebase API Key or

b) Set up Firebase yourself

## Firebase Setup

Create a ```.env``` file in the main directory and insert your Firebase configuration in the format below: 

```{r} 
apiKey=""
authDomain=""
projectId=""
storageBucket=""
messagingSenderId=""
appId=""
measurementId="" 
```
## Unsure how to obtain firebase configuration?

Go to ```https://console.firebase.google.com/```. create an account if you do not have one already

Click on ```Add Project```

Give your project any name and click next

Enable Google Analytics and click next

Choose ```Default Account for Firebase``` and click next

Under Authentication, click get started on sign-in methods and enable Email/Password. There is no need to enable 'Email link (passwordless sign-in)'

Under Firebase Database, click create database and start ```in test mode```

Select the default Cloud Firestore location and click enable

On the home page, add a web app to get started and give it a name. Click register.

Copy the values under ```const firebaseConfig``` into your .env file as stated above

