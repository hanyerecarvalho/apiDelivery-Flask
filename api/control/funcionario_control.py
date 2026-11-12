from flask import jsonify, request


class FuncionarioControl:
    def __init__(self, funcionario_service):
        self.__funcionario_service = funcionario_service

    def login(self):
        body = request.get_json(silent=True)
        dados = body.get("funcionario", body) if isinstance(body, dict) else {}
        if not isinstance(dados, dict):
            dados = {}
        email = dados.get("email")
        senha = dados.get("senha")
        if (not isinstance(email, str) or not email.strip() or len(email) > 254
                or not isinstance(senha, str) or not senha or len(senha) > 1024):
            return jsonify(success=False, message="Informe e-mail e senha."), 400

        token = self.__funcionario_service.login(email.strip().lower(), senha)
        if not token:
            return jsonify(success=False, message="E-mail ou senha incorretos."), 401

        resposta = jsonify(success=True, data={"token": token})
        resposta.headers["Cache-Control"] = "no-store"
        return resposta
