from flask import Blueprint, request, jsonify, current_app
from config.firebase import db
from models.Client import Client
from flask import render_template

import bcrypt
import jwt
import datetime

client_bp = Blueprint('clients', __name__)

@client_bp.route('/inscription', methods=['POST'])
def inscription():
    data = request.json
    if not data or not all(k in data for k in ("nom", "telephone", "adresse", "mot_de_passe")):
        return jsonify({"message": "Données incomplètes"}), 400

    # Vérifier si le téléphone existe déjà
    users = db.child("clients").order_by_child("telephone").equal_to(data["telephone"]).get()
    if users.each():
        return jsonify({"message": "Ce numéro est déjà utilisé"}), 400

    # Création du client
    client = Client(data["nom"], data["telephone"], data["adresse"], data["mot_de_passe"])
    db.child("clients").push(client.to_dict())

    return jsonify({"message": "Compte créé avec succès"}), 201

@client_bp.route('/connexion', methods=['POST'])
def connexion():
    data = request.json
    if not data or not all(k in data for k in ("telephone", "mot_de_passe")):
        return jsonify({"message": "Données incomplètes"}), 400

    # Recherche du client par téléphone
    users = db.child("clients").order_by_child("telephone").equal_to(data["telephone"]).get()
    user_data = None
    user_id = None
    for user in users.each():
        user_data = user.val()
        user_id = user.key()
        break

    if not user_data:
        return jsonify({"message": "Numéro de téléphone incorrect"}), 400

    # Vérification du mot de passe
    if not bcrypt.checkpw(data["mot_de_passe"].encode('utf-8'), user_data["mot_de_passe"].encode('utf-8')):
        return jsonify({"message": "Mot de passe incorrect"}), 400

    return jsonify({"message": "Connexion réussie", "id_client": user_id}), 200

@client_bp.route('/profil', methods=['GET'])
def profil():
    id_client = request.args.get("id_client")
    
    if not id_client:
        return jsonify({"message": "ID du client requis"}), 400

    client_data = db.child("clients").child(id_client).get().val()

    if not client_data:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

    return jsonify(client_data), 200

@client_bp.route('/modifier', methods=['PUT'])
def modifier_profil():
    data = request.get_json()

    if not all(k in data for k in ("id_client", "nom", "adresse", "mot_de_passe")):
        return jsonify({"message": "Données incomplètes"}), 400

    # Vérifier si l'utilisateur existe
    client_ref = db.child("clients").child(data["id_client"]).get()
    if not client_ref.val():
        return jsonify({"message": "Utilisateur introuvable"}), 404

    # Mise à jour des informations
    db.child("clients").child(data["id_client"]).update({
        "nom": data["nom"],
        "adresse": data["adresse"],
        "mot_de_passe": Client.hash_mot_de_passe(data["mot_de_passe"])  # Hachage du mot de passe
    })

    return jsonify({"message": "Profil mis à jour avec succès"}), 200

@client_bp.route('/supprimer', methods=['DELETE'])
def supprimer_client():
    data = request.get_json()

    if "id_client" not in data:
        return jsonify({"message": "ID du client requis"}), 400

    client_ref = db.child("clients").child(data["id_client"]).get()
    if not client_ref.val():
        return jsonify({"message": "Utilisateur introuvable"}), 404

    # Suppression du client
    db.child("clients").child(data["id_client"]).remove()

    return jsonify({"message": "Utilisateur supprimé avec succès"}), 200

from flask import jsonify

@client_bp.route('/index_clients', methods=['GET'])
def index_clients():
    """Retourne la liste des clients au format JSON"""
    clients = db.child("clients").get()

    if not clients.val():
        return jsonify({"clients": []})  # Retourner une liste vide

    # Transformer les données en liste
    clients_list = [{"id": key, **value} for key, value in clients.val().items()]
    
    return jsonify({"clients": clients_list})  # Retourner en JSON


@client_bp.route('/derniers_clients', methods=['GET'])
def derniers_clients():
    """Récupère les 5 derniers clients enregistrés pour affichage sur le dashboard"""
    clients = db.child("clients").get()

    if not clients.val():
        return jsonify({"clients": []}), 200

    # Transformer les données en une liste triée par ordre d'ajout
    clients_list = [{"id": key, **value} for key, value in clients.val().items()]

    # Récupérer les 5 derniers clients
    derniers_clients = sorted(clients_list, key=lambda x: x.get("date_creation", ""), reverse=True)[:7]

    return jsonify({"clients": derniers_clients}), 200

@client_bp.route('/clients', methods=['GET'])
def clients_page():
    """Affiche la page HTML des clients"""
    return render_template("clients/index.html")