from flask import Flask, session, render_template, request, redirect, url_for, flash
from config.firebase import auth  # Import de Firebase
from routes.boissons import boisson_bp  # Import du Blueprint
from routes.agences import agence_bp  # Import du Blueprint
from routes.livreurs import livreur_bp  # Import du Blueprint
from routes.commandes import commande_bp 
from routes.clients import client_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = "ICI"


# Enregistrement du Blueprint
app.register_blueprint(boisson_bp, url_prefix='/Boissons')
app.register_blueprint(agence_bp, url_prefix='/Agences')
app.register_blueprint(livreur_bp, url_prefix='/Livreurs')
app.register_blueprint(client_bp, url_prefix='/clients')
app.register_blueprint(commande_bp, url_prefix='/commandes')



# Page d'accueil après connexion
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('main.html')
    else:
        return redirect(url_for('login'))

# Page de connexion
@app.route('/', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect(url_for('home'))
        except:
            flash("Email ou mot de passe incorrect.", "danger")
            return render_template('index.html')

    return render_template('index.html')

# Route de déconnexion
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=5050, debug=True)

