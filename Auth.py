import pyrebase

config ={
    'apiKey': "AIzaSyCRP-v1s0Ih5Fjniku3U0AvzlQrGK8UPJQ",
    'authDomain': "flaskauth-66dbe.firebaseapp.com",
    'projectId': "flaskauth-66dbe",
    'storageBucket': "flaskauth-66dbe.firebasestorage.app",
    'messagingSenderId': "666631576308",
    'appId': "1:666631576308:web:f38968e434d054af8adca1",
    'measurementId': "G-80TSLBRXNG",
    'databaseURL': 'https://flaskauth-66dbe-default-rtdb.firebaseio.com/'   
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()



email = "admin@gmail.com"
password = "isaac0524"

user = auth.create_user_with_email_and_password(email,password)
print(user)

#user = auth.sign_in_with_email_and_password(email,password)
#print(user)

