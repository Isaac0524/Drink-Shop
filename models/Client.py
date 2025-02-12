import bcrypt
import time

class Client:
    def __init__(self, nom, telephone, adresse, mot_de_passe, id_client=None, date_inscription=None):
        self.id_client = id_client
        self.nom = nom
        self.telephone = telephone
        self.adresse = adresse
        self.mot_de_passe = self.hash_mot_de_passe(mot_de_passe) if mot_de_passe else None
        self.date_inscription = date_inscription if date_inscription else int(time.time())

    @staticmethod
    def hash_mot_de_passe(mot_de_passe):
        """Hache le mot de passe avant stockage"""
        return bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verifier_mot_de_passe(self, mot_de_passe):
        """Vérifie si un mot de passe correspond au hash enregistré"""
        return bcrypt.checkpw(mot_de_passe.encode('utf-8'), self.mot_de_passe.encode('utf-8'))

    def to_dict(self):
        """Convertit l'objet en dictionnaire pour Firebase"""
        return {
            "nom": self.nom,
            "telephone": self.telephone,
            "adresse": self.adresse,
            "mot_de_passe": self.mot_de_passe,  # Toujours stocké en hashé
            "date_inscription": self.date_inscription
        }
