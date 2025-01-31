from flask import Flask, session, render_template, request, redirect, url_for, flash
import pyrebase

app = Flask(__name__)

# Configuration de Firebase
config = {
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

app.secret_key = 'secret'


# Page d'accueil après connexion (redirige l'utilisateur si connecté)
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('main.html')  # Accueil de l'utilisateur
    else:
        return redirect(url_for('login'))  # Redirige vers la page de connexion si non connecté


# Page de connexion
@app.route('/', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))  # Si déjà connecté, redirige vers l'accueil

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email  # Enregistrer l'utilisateur dans la session
            return redirect(url_for('home'))  # Rediriger vers la page d'accueil après connexion
        except:
            flash("Email ou mot de passe incorrect. Veuillez réessayer.", "danger")
            return render_template('index.html')

    return render_template('index.html')  # Affiche la page de connexion


# Route de déconnexion
@app.route('/logout')
def logout():
    session.pop('user', None)  # Supprime l'utilisateur de la session
    return redirect('/')  # Redirige vers la page de connexion


if __name__ == '__main__':
    app.run(port=5050)
