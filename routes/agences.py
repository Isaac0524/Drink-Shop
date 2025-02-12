from flask import Blueprint, request, jsonify, render_template
from models.Agence import Agence

agence_bp = Blueprint('agence_bp', __name__)

@agence_bp.route('/agences', methods=['POST'])
def add_agence():
    """Ajoute une nouvelle agence"""
    data = request.json
    if not all(k in data for k in ("nom", "adresse", "telephone")):
        return jsonify({"message": "Données incomplètes"}), 400

    agence = Agence(**data)
    agence.save()
    return jsonify({"message": "Agence ajoutée avec succès", "agence": agence.to_dict()}), 201


@agence_bp.route('/agences', methods=['GET'])
def get_agences():
    """Récupère toutes les agences"""
    agences = Agence.get_all()
    return jsonify([agence.to_dict() for agence in agences]), 200


@agence_bp.route('/agences/<agence_id>', methods=['GET'])
def get_agence(agence_id):
    """Récupère une agence spécifique"""
    agence = Agence.get_by_id(agence_id)
    if not agence:
        return jsonify({"message": "Agence introuvable"}), 404
    return jsonify(agence), 200


@agence_bp.route('/agences/<agence_id>', methods=['PUT'])
def update_agence(agence_id):
    """Met à jour une agence"""
    data = request.json
    if not data:
        return jsonify({"message": "Aucune donnée fournie"}), 400

    Agence.update(agence_id, data)
    return jsonify({"message": "Agence mise à jour avec succès"}), 200


@agence_bp.route('/agences/<agence_id>', methods=['DELETE'])
def delete_agence(agence_id):
    """Supprime une agence"""
    Agence.delete(agence_id)
    return jsonify({"message": "Agence supprimée avec succès"}), 200

@agence_bp.route('/gestion_agences', methods=['GET'])
def gestionAgences():
    """Rend la page HTML pour la gestion des agences"""
    return render_template('agences/agences.html')
