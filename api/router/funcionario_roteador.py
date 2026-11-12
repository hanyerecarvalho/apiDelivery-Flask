from flask import Blueprint


class FuncionarioRoteador:
    def __init__(self, funcionario_control):
        self.__funcionario_control = funcionario_control

    def create_routes(self):
        blueprint = Blueprint("funcionarios", __name__)

        @blueprint.post("/login")
        def login():
            return self.__funcionario_control.login()

        return blueprint
