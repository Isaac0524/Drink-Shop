from flask import Blueprint, request, jsonify, session
from models.Commande import Commande
from config.firebase import db

commande_bp = Blueprint('commandes', __name__)

@commande_bp.route('/ajouter_boisson', methods=['POST'])
def ajouter_boisson():
    if "user_id" not in session:
        return jsonify({"message": "Veuillez vous connecter"}), 401

    data = request.json
    if not data or "nom_boisson" not in data or "quantite" not in data:
        return jsonify({"message": "Données invalides"}), 400

    client_id = session["user_id"]
    panier = db.child("paniers").child(client_id).get().val() or []
    panier.append({"nom": data["nom_boisson"], "quantite": data["quantite"]})
    db.child("paniers").child(client_id).set(panier)

    return jsonify({"message": "Boisson ajoutée", "panier": panier}), 200

@commande_bp.route('/voir_panier', methods=['GET'])
def voir_panier():
    if "user_id" not in session:
        return jsonify({"message": "Veuillez vous connecter"}), 401

    client_id = session["user_id"]
    panier = db.child("paniers").child(client_id).get().val() or []

    return jsonify({"panier": panier}), 200

@commande_bp.route('/confirmer_commande', methods=['POST'])
def confirmer_commande():
    if "user_id" not in session:
        return jsonify({"message": "Veuillez vous connecter"}), 401

    client_id = session["user_id"]
    panier = db.child("paniers").child(client_id).get().val()

    if not panier:
        return jsonify({"message": "Votre panier est vide"}), 400

    commande = Commande(client_id, panier)
    commande.save_to_firebase()
    db.child("paniers").child(client_id).remove()

    return jsonify({"message": "Commande enregistrée", "commande": commande.to_dict()}), 201

@commande_bp.route('/commandes', methods=['GET'])
def liste_commandes():
    if "user_id" not in session:
        return jsonify({"message": "Veuillez vous connecter"}), 401

    client_id = session["user_id"]
    commandes = db.child("commandes").order_by_child("client_id").equal_to(client_id).get().val()

    if not commandes:
        return jsonify({"message": "Aucune commande trouvée"}), 404

    return jsonify({"commandes": commandes}), 200
