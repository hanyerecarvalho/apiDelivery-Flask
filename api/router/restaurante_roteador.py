# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.restaurante_middleware import RestauranteMiddleware
from api.control.restaurante_control import RestauranteControl

class RestauranteRoteador:
    def __init__(self, jwt_middleware: JwtMiddleware, restaurante_middleware: RestauranteMiddleware, restaurante_control: RestauranteControl):
        print("⬆️  RestauranteRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__restaurante_middleware = restaurante_middleware
        self.__restaurante_control = restaurante_control

        # Blueprint é a coleção de rotas da entidade Cargo
        self.__blueprint = Blueprint('restaurante', __name__)

    def create_routes(self):
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__restaurante_middleware.validate_body  # valida corpo da requisição
        def store():
            return self.__restaurante_control.store()

        # GET / -> lista todos os cargos
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token  # valida token JWT
        def index():
            """
            Rota responsável por listar todos os cargos cadastrados no sistema.
            """
            return self.__restaurante_control.index()

        # GET /<idCargo> -> retorna um cargo específico
        @self.__blueprint.route('/<int:idRestaurante>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__restaurante_middleware.validate_id_param  # valida se o ID é válido
        def show(idRestaurante):
            """
            Rota que retorna um cargo específico pelo seu ID.

            :param idCargo: int - ID do cargo vindo da URI.
            """
            return self.__restaurante_control.show(idRestaurante)

        # PUT /<idCargo> -> atualiza um cargo
        @self.__blueprint.route('/<int:idRestaurante>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__restaurante_middleware.validate_id_param
        @self.__restaurante_middleware.validate_body
        def update(idRestaurante):
            return self.__restaurante_control.update()

        # DELETE /<idCargo> -> remove um cargo
        @self.__blueprint.route('/<int:idRestaurante>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__restaurante_middleware.validate_id_param
        def destroy(idRestaurante):
            """
            Rota que remove um cargo pelo seu ID.

            :param idCargo: int - ID do cargo a ser removido.
            """
            return self.__restaurante_control.destroy()

        return self.__blueprint