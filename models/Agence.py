from config.firebase import db
import uuid
from models.Boisson import Boisson  # Import du modèle Boisson

class Agence:
    def __init__(self, nom, adresse, telephone, stock_boissons=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.nom = nom
        self.adresse = adresse
        self.telephone = telephone
        self.stock_boissons = stock_boissons or {}  # Dictionnaire, pas liste

    def to_dict(self):
        """Convertit l'agence en dictionnaire"""
        return {
            "id": self.id,
            "nom": self.nom,
            "adresse": self.adresse,
            "telephone": self.telephone,
            "stock_boissons": [self.format_boisson(b) for b in self.stock_boissons.values()] if isinstance(self.stock_boissons, dict) else []
  # Assurez-vous que `stock_boissons` est un dictionnaire
        }

    
    def format_boisson(self, boisson):
        """Convertit le dictionnaire de boisson en format exploitable pour JSON"""
        return {
            "id_boisson": boisson.get("id_boisson"),
            "nom": boisson.get("nom"),
            "quantite": boisson.get("quantite")
        }

    def save(self):
        """Ajoute ou met à jour une agence dans Firebase"""
        db.child("agences").child(self.id).set(self.to_dict())

    @staticmethod
    def get_all():
        """Récupère toutes les agences avec les noms des boissons"""
        agences_data = db.child("agences").get()
        if not agences_data.val():
            return []
        
        agences = []
        for agence_data in agences_data.each():  # Chaque agence dans Firebase
            data = agence_data.val()
            
            # Vérification de la présence de la clé 'stock_boissons', et s'il est absent, utiliser un dictionnaire vide
            stock_boissons = data.get("stock_boissons", {})  # Assurez-vous que stock_boissons est un dictionnaire
            
            # Crée une instance de Agence pour chaque agence récupérée
            agence = Agence(
                id=agence_data.key(),  # Utiliser l'ID de l'agence comme clé
                nom=data["nom"],
                adresse=data["adresse"],
                telephone=data["telephone"],
                stock_boissons=stock_boissons
            )
            agences.append(agence)
        
        return agences


    @staticmethod
    def get_by_id(agence_id):
        """Récupère une agence spécifique avec les boissons"""
        agence = db.child("agences").child(agence_id).get()
        return agence.val() if agence.val() else None

    def ajouter_boisson(self, id_boisson, quantite):
        """Ajoute une boisson à l'agence en vérifiant le stock global"""
        boisson = Boisson.get_by_id(id_boisson)
        if not boisson:
            return {"message": "Boisson introuvable"}, 404

        if boisson["stock"] < quantite:
            return {"message": "Stock insuffisant dans l'entrepôt"}, 400

        # Décrémenter le stock global
        new_stock = boisson["stock"] - quantite
        Boisson.update(id_boisson, {"stock": new_stock})  # Met à jour Firebase

        # Ajouter la boisson à l'agence avec son nom
        if "stock_boissons" not in self.__dict__:
            self.stock_boissons = {}

        self.stock_boissons[id_boisson] = {
            "nom": boisson.get("nom", "Nom inconnu"),
            "quantite": quantite
        }
        
        self.save()

        return {"message": "Boisson ajoutée avec succès", "stock_boissons": self.stock_boissons}, 200


    @staticmethod
    def update(agence_id, data):
        """Met à jour les informations d'une agence"""
        db.child("agences").child(agence_id).update(data)

    @staticmethod
    def delete(agence_id):
        """Supprime une agence"""
        db.child("agences").child(agence_id).remove()
