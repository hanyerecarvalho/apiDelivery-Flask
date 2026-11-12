import hashlib
import hmac
import re

from api.middleware.jwt_middleware import MeuTokenJWT


class FuncionarioService:
    def __init__(self, funcionario_dao):
        self.__funcionario_dao = funcionario_dao

    def login(self, email, senha):
        funcionario = self.__funcionario_dao.buscar_por_email(email)
        if not funcionario:
            return None

        registro = funcionario.senha_hash
        if not re.fullmatch(r"[0-9a-f]{32}:[0-9a-f]{128}", registro):
            return None

        salt, hash_salvo = registro.split(":")
        # Mesmo formato usado por apiJs4bi: salt em texto hexadecimal e hash de 64 bytes.
        hash_informado = hashlib.scrypt(
            senha.encode("utf-8"), salt=salt.encode("ascii"), n=16384, r=8, p=1, dklen=64
        )
        if not hmac.compare_digest(hash_informado, bytes.fromhex(hash_salvo)):
            return None

        return MeuTokenJWT().gerar_token({
            "idFuncionario": funcionario.id_funcionario,
            "email": funcionario.email,
            "name": funcionario.nome,
            "role": "funcionario",
        })
