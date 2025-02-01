from flask import Blueprint, request, jsonify
from models.Boisson import Boisson

boisson_bp = Blueprint('boisson_bp', __name__)

@boisson_bp.route('/boissons', methods=['POST'])
def add_boisson():
    """Ajoute une nouvelle boisson"""
    data = request.json
    if not all(k in data for k in ("nom", "categorie", "volume", "prix_unitaire", "stock")):
        return jsonify({"message": "Données incomplètes"}), 400
    
    boisson = Boisson(**data)
    boisson.save()
    return jsonify({"message": "Boisson ajoutée avec succès", "boisson": boisson.to_dict()}), 201


@boisson_bp.route('/boissons', methods=['GET'])
def get_boissons():
    """Récupère toutes les boissons"""
    return jsonify(Boisson.get_all()), 200


@boisson_bp.route('/boissons/<boisson_id>', methods=['GET'])
def get_boisson(boisson_id):
    """Récupère une boisson spécifique"""
    boisson = Boisson.get_by_id(boisson_id)
    if not boisson:
        return jsonify({"message": "Boisson introuvable"}), 404
    return jsonify(boisson), 200


@boisson_bp.route('/boissons/<boisson_id>', methods=['PUT'])
def update_boisson(boisson_id):
    """Met à jour une boisson"""
    data = request.json
    if not data:
        return jsonify({"message": "Aucune donnée fournie"}), 400
    
    Boisson.update(boisson_id, data)
    return jsonify({"message": "Boisson mise à jour avec succès"}), 200


@boisson_bp.route('/boissons/<boisson_id>', methods=['DELETE'])
def delete_boisson(boisson_id):
    """Supprime une boisson"""
    Boisson.delete(boisson_id)
    return jsonify({"message": "Boisson supprimée avec succès"}), 200
