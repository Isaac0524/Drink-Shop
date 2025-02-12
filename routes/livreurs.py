from flask import Blueprint, request, jsonify
from models.livreur import Livreur

livreur_bp = Blueprint('livreurs', __name__)

@livreur_bp.route('/ajouter', methods=['POST'])
def add_livreur():
    """Ajoute un nouveau livreur (créé par l'admin)"""
    data = request.json
    if not all(k in data for k in ("nom", "telephone", "agence_id", "mot_de_passe")):
        return jsonify({"message": "Données incomplètes"}), 400

    livreur_id, livreur_exist = Livreur.get_by_telephone(data["telephone"])
    if livreur_exist:
        return jsonify({"message": "Ce numéro de téléphone est déjà utilisé"}), 400

    # Création du livreur
    livreur = Livreur(**data)
    livreur.save()
    return jsonify({"message": "Livreur ajouté avec succès", "livreur": livreur.to_dict()}), 201


@livreur_bp.route('/livreurs', methods=['GET'])
def get_livreurs():
    """Récupère tous les livreurs"""
    return jsonify(Livreur.get_all()), 200


@livreur_bp.route('/<livreur_id>', methods=['GET'])
def get_livreur(livreur_id):
    """Récupère un livreur spécifique"""
    livreur_data = Livreur.get_by_id(livreur_id)
    if not livreur_data:
        return jsonify({"message": "Livreur introuvable"}), 404
    return jsonify(livreur_data), 200


@livreur_bp.route('/<livreur_id>', methods=['PUT'])
def update_livreur(livreur_id):
    """Met à jour un livreur"""
    data = request.json
    if not data:
        return jsonify({"message": "Aucune donnée fournie"}), 400

    Livreur.update(livreur_id, data)
    return jsonify({"message": "Livreur mis à jour avec succès"}), 200


@livreur_bp.route('/<livreur_id>', methods=['DELETE'])
def delete_livreur(livreur_id):
    """Supprime un livreur"""
    Livreur.delete(livreur_id)
    return jsonify({"message": "Livreur supprimé avec succès"}), 200


@livreur_bp.route('/<livreur_id>/livraisons', methods=['POST'])
def enregistrer_livraison(livreur_id):
    """Ajoute une livraison au suivi des performances du livreur"""
    data = request.json
    if "boissons_livrees" not in data:
        return jsonify({"message": "Nombre de boissons livrées requis"}), 400

    livreur_data = Livreur.get_by_id(livreur_id)
    if not livreur_data:
        return jsonify({"message": "Livreur introuvable"}), 404

    livreur_obj = Livreur(**livreur_data)
    livreur_obj.enregistrer_livraison(data["boissons_livrees"])
    livreur_obj.save()

    return jsonify({"message": "Livraison enregistrée avec succès", "performances": livreur_obj.performances}), 200


@livreur_bp.route('/connexion', methods=['POST'])
def connexion_livreur():
    data = request.json
    if not data or not all(k in data for k in ("telephone", "mot_de_passe")):
        return jsonify({"message": "Données incomplètes"}), 400

    livreur_id, livreur_data = Livreur.get_by_telephone(data["telephone"])
    if not livreur_data:
        return jsonify({"message": "Numéro de téléphone incorrect"}), 400

    # Vérifier le mot de passe
    livreur_obj = Livreur(**livreur_data)
    if not livreur_obj.verifier_mot_de_passe(data["mot_de_passe"]):
        return jsonify({"message": "Mot de passe incorrect"}), 400

    return jsonify({"message": "Connexion réussie", "id_livreur": livreur_id}), 200


@livreur_bp.route('/modifier', methods=['PUT'])
def modifier_livreur():
    data = request.json
    if not all(k in data for k in ("id_livreur", "nom", "agence_id")):
        return jsonify({"message": "Données incomplètes"}), 400

    # Vérifier si le livreur existe
    livreur_data = Livreur.get_by_id(data["id_livreur"])
    if not livreur_data:
        return jsonify({"message": "Livreur introuvable"}), 404

    # Mise à jour
    Livreur.update(data["id_livreur"], {
        "nom": data["nom"],
        "agence_id": data["agence_id"]
    })

    return jsonify({"message": "Profil mis à jour avec succès"}), 200


@livreur_bp.route('/modifier_mdp', methods=['PUT'])
def modifier_mdp_livreur():
    data = request.json
    if not all(k in data for k in ("id_livreur", "ancien_mdp", "nouveau_mdp")):
        return jsonify({"message": "Données incomplètes"}), 400

    # Vérifier si le livreur existe
    livreur_data = Livreur.get_by_id(data["id_livreur"])
    if not livreur_data:
        return jsonify({"message": "Livreur introuvable"}), 404

    livreur_obj = Livreur(**livreur_data)
    
    # Vérifier l'ancien mot de passe
    if not livreur_obj.verifier_mot_de_passe(data["ancien_mdp"]):
        return jsonify({"message": "Ancien mot de passe incorrect"}), 400

    # Mettre à jour le mot de passe
    nouveau_mdp_hache = Livreur.hash_mot_de_passe(data["nouveau_mdp"])
    Livreur.update(data["id_livreur"], {"mot_de_passe": nouveau_mdp_hache})

    return jsonify({"message": "Mot de passe mis à jour avec succès"}), 200
