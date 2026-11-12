# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.pedido_middleware import PedidoMiddleware
from api.control.pedido_control import PedidoControl

class PedidoRoteador:
    def __init__(self, jwt_middleware: JwtMiddleware, pedido_middleware: PedidoMiddleware, pedido_control: PedidoControl):
        print("⬆️  PedidoRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__pedido_middleware = pedido_middleware
        self.__pedido_control = pedido_control

        # Blueprint é a coleção de rotas da entidade Cargo
        self.__blueprint = Blueprint('pedido', __name__)

    def create_routes(self):
        @self.__blueprint.route('/', strict_slashes=False, methods=['POST'])
        @self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__pedido_middleware.validate_body  # valida corpo da requisição
        def store():
            return self.__pedido_control.store()

        # GET / -> lista todos os cargos
        @self.__blueprint.route('/', strict_slashes=False, methods=['GET'])
        @self.__jwt_middleware.validate_token  # valida token JWT
        def index():
            """
            Rota responsável por listar todos os cargos cadastrados no sistema.
            """
            return self.__pedido_control.index()

        # GET /<idCargo> -> retorna um cargo específico
        @self.__blueprint.route('/<int:idPedido>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__pedido_middleware.validate_id_param  # valida se o ID é válido
        def show(idPedido):
            """
            Rota que retorna um cargo específico pelo seu ID.

            :param idCargo: int - ID do cargo vindo da URI.
            """
            return self.__pedido_control.show()

        # PUT /<idCargo> -> atualiza um cargo
        @self.__blueprint.route('/<int:idPedido>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__pedido_middleware.validate_id_param
        @self.__pedido_middleware.validate_body
        def update(idPedido):
            return self.__pedido_control.update()

        # DELETE /<idCargo> -> remove um cargo
        @self.__blueprint.route('/<int:idPedido>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__pedido_middleware.validate_id_param
        def destroy(idPedido):
            """
            Rota que remove um cargo pelo seu ID.

            :param idCargo: int - ID do cargo a ser removido.
            """
            return self.__pedido_control.destroy()

        return self.__blueprint
