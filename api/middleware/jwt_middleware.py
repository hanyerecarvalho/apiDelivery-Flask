import os
from pathlib import Path
import jwt
import time
import secrets
from flask import request, jsonify
from functools import wraps


class MeuTokenJWT:
    """Classe para gerar e validar tokens JWT"""
    
    def __init__(self):
        self._key = os.environ.get("FLASK_JWT_SECRET")
        if not self._key:
            arquivo = Path(__file__).resolve().parents[2] / ".jwt-secret"
            if arquivo.is_file():
                self._key = arquivo.read_text(encoding="utf-8").strip()
        if not self._key or len(self._key) < 32:
            raise RuntimeError("Configure FLASK_JWT_SECRET ou o arquivo .jwt-secret.")
        self._alg = "HS256"
        self._iss = "http://localhost"
        self._aud = "http://localhost"
        self._sub = "acesso_sistema"
        self._duracao_token = 3600  # Uma hora
        self._payload = None

    @property
    def payload(self):
        return self._payload

    def gerar_token(self, claims: dict) -> str:
        payload = {
            "iss": self._iss,
            "aud": self._aud,
            "sub": self._sub,
            "iat": int(time.time()),
            "exp": int(time.time()) + self._duracao_token,
            "nbf": int(time.time()),
            "jti": secrets.token_hex(16),
            **claims
        }
        token = jwt.encode(payload, self._key, algorithm=self._alg)
        return token

    def validar_token(self, token: str) -> bool:
        if not token:
            print("Token não fornecido")
            return False

        token = token.replace("Bearer ", "").strip()

        try:
            decoded = jwt.decode(token, self._key, algorithms=[self._alg], audience=self._aud, issuer=self._iss)
            self._payload = decoded
            return True
        except jwt.ExpiredSignatureError:
            print("Token expirado")
        except jwt.InvalidTokenError:
            print("Token inválido")
        return False


class JwtMiddleware:
    """Middleware Flask para validação de tokens JWT"""

    def validate_token(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 JwtMiddleware.validate_token()")
            authorization = request.headers.get("Authorization", None)
            jwt_instance = MeuTokenJWT()

            if jwt_instance.validar_token(authorization):
                return f(*args, **kwargs)
            else:
                return jsonify({"status": False, "msg": "token inválido"}), 401

        return decorated_function
