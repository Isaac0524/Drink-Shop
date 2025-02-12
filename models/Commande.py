import uuid
from config.firebase import db

class Commande:
    def __init__(self, client_id, articles, status="en_attente"):
        self.id = f"cmd_{uuid.uuid4().hex[:8]}"  # ID unique
        self.client_id = client_id
        self.articles = articles  # Liste de boissons {nom, quantité}
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "articles": self.articles,
            "status": self.status
        }

    def save_to_firebase(self):
        db.child("commandes").child(self.id).set(self.to_dict())
