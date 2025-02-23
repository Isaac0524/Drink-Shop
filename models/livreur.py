from config.firebase import db
import uuid
import bcrypt
from datetime import datetime

class Livreur:
    def __init__(self, nom, telephone, agence_id, mot_de_passe, performances=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.nom = nom
        self.telephone = telephone
        self.agence_id = agence_id
        self.mot_de_passe = self.hash_mot_de_passe(mot_de_passe)  # Hachage du mot de passe
        self.performances = performances or {}  

    @staticmethod
    def hash_mot_de_passe(mot_de_passe):
        """Hache le mot de passe avant stockage"""
        return bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verifier_mot_de_passe(self, mot_de_passe):
        """Vérifie si le mot de passe correspond au hash"""
        return bcrypt.checkpw(mot_de_passe.encode('utf-8'), self.mot_de_passe.encode('utf-8'))

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "telephone": self.telephone,
            "agence_id": self.agence_id,
            "mot_de_passe": self.mot_de_passe,
            "performances": self.performances
        }

    def save(self):
        """Ajoute ou met à jour un livreur dans Firebase"""
        db.child("livreurs").child(self.id).set(self.to_dict())

    @staticmethod
    def get_by_telephone(telephone):
        """Récupère un livreur par son numéro de téléphone"""
        livreurs = db.child("livreurs").order_by_child("telephone").equal_to(telephone).get()
        for livreur in livreurs.each():
            return livreur.key(), livreur.val()
        return None, None
    
    @staticmethod
    def get_all():
        """Récupère tous les livreurs depuis Firebase"""
        livreurs = db.child("livreurs").get().val()
        if not livreurs:
            return []
        
        # Convertir le dictionnaire Firebase en liste
        return [{"id": key, **value} for key, value in livreurs.items()]