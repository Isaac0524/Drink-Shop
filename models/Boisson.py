import uuid
from config.firebase import db  # Import de la connexion Firebase

class Boisson:
    def __init__(self, nom: str, categorie: str, volume: float, prix_unitaire: float, stock: int, id: str = None):
        self.id = id if id else str(uuid.uuid4())
        self.nom = nom
        self.categorie = categorie
        self.volume = volume
        self.prix_unitaire = prix_unitaire
        self.stock = stock

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "categorie": self.categorie,
            "volume": self.volume,
            "prix_unitaire": self.prix_unitaire,
            "stock": self.stock
        }

    def save(self) -> None:
        """Sauvegarde la boisson dans Firebase"""
        db.child("boissons").child(self.id).set(self.to_dict())

    @staticmethod
    def get_all() -> list[dict]:
        """Récupère toutes les boissons"""
        boissons = db.child("boissons").get()
        return [boisson.val() for boisson in boissons.each()] if boissons.each() else []

    @staticmethod
    def get_by_id(boisson_id: str) -> dict | None:
        """Récupère une boisson spécifique par ID"""
        boisson = db.child("boissons").child(boisson_id).get()
        return boisson.val() if boisson.val() else None

    @staticmethod
    def update(boisson_id: str, data: dict) -> None:
        """Met à jour une boisson"""
        db.child("boissons").child(boisson_id).update(data)

    @staticmethod
    def delete(boisson_id: str) -> None:
        """Supprime une boisson"""
        db.child("boissons").child(boisson_id).remove()
