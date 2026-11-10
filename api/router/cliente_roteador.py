# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.cliente_middleware import ClienteMiddleware
from api.control.cliente_control import ClienteControl

class ClienteRoteador:
    def __init__(self, jwt_middleware: JwtMiddleware, cliente_middleware: ClienteMiddleware, cliente_control: ClienteControl):
        print("⬆️  ClienteRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__cliente_middleware = cliente_middleware
        self.__cliente_control = cliente_control

        # Blueprint é a coleção de rotas da entidade Cargo
        self.__blueprint = Blueprint('cliente', __name__)

    def create_routes(self):
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__cliente_middleware.validate_body  # valida corpo da requisição
        def store():
            return self.__cliente_control.store()

        # GET / -> lista todos os cargos
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token  # valida token JWT
        def index():
            """
            Rota responsável por listar todos os cargos cadastrados no sistema.
            """
            return self.__cliente_control.index()

        # GET /<idCargo> -> retorna um cargo específico
        @self.__blueprint.route('/<int:idCliente>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__cliente_middleware.validate_id_param  # valida se o ID é válido
        def show(idCliente):
            """
            Rota que retorna um cargo específico pelo seu ID.

            :param idCargo: int - ID do cargo vindo da URI.
            """
            return self.__cliente_control.show(idCliente)

        # PUT /<idCargo> -> atualiza um cargo
        @self.__blueprint.route('/<int:idCliente>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__cliente_middleware.validate_id_param
        @self.__cliente_middleware.validate_body
        def update(idCliente):
            return self.__cliente_control.update()

        # DELETE /<idCargo> -> remove um cargo
        @self.__blueprint.route('/<int:idCliente>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__cliente_middleware.validate_id_param
        def destroy(idCliente):
            """
            Rota que remove um cargo pelo seu ID.

            :param idCargo: int - ID do cargo a ser removido.
            """
            return self.__cliente_control.destroy()

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint