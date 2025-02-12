from flask import request, jsonify
import jwt
from functools import wraps
from flask import current_app

def token_requis(f):
    @wraps(f)
    def decorateur(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token manquant"}), 401

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.id_client = data["id_client"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expiré"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token invalide"}), 401

        return f(*args, **kwargs)

    return decorateur
