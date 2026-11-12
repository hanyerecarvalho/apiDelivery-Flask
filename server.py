from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from werkzeug.exceptions import HTTPException, NotFound

from api.database.mysql_database import MysqlDatabase
from api.utils.error_response import ErrorResponse
from api.utils.logger import Logger

from api.middleware.jwt_middleware import JwtMiddleware, MeuTokenJWT
from api.dao.funcionario_dao import FuncionarioDAO
from api.service.funcionario_service import FuncionarioService
from api.control.funcionario_control import FuncionarioControl
from api.router.funcionario_roteador import FuncionarioRoteador
from api.middleware.cliente_middleware import ClienteMiddleware
from api.middleware.pedido_middleware import PedidoMiddleware
from api.middleware.restaurante_middleware import RestauranteMiddleware

from api.control.cliente_control import ClienteControl
from api.control.pedido_control import PedidoControl
from api.control.restaurante_control import RestauranteControl

from api.service.cliente_service import ClienteService
from api.service.pedido_service import PedidoService
from api.service.restaurante_service import RestauranteService

from api.dao.cliente_dao import ClienteDAO
from api.dao.pedido_dao import PedidoDAO
from api.dao.restaurante_dao import RestauranteDAO

from api.router.cliente_roteador import ClienteRoteador
from api.router.pedido_roteador import PedidoRoteador
from api.router.restaurante_roteador import RestauranteRoteador

import traceback


class Server:

    def __init__(self, porta: int = 8080):
        self.__porta = porta

        self.__app = Flask(__name__, static_folder="static", static_url_path="")

        CORS(self.__app, resources={r"/*": {"origins": "*"}})

        self.__jwt_middleware = JwtMiddleware()
        self.__cliente_middleware = ClienteMiddleware()
        self.__pedido_middleware = PedidoMiddleware()
        self.__restaurante_middleware = RestauranteMiddleware()

        self.__cliente_dao = None
        self.__pedido_dao = None
        self.__restaurante_dao = None
        
        self.__cliente_service = None
        self.__pedido_service = None
        self.__restaurante_service = None
        
        self.__cliente_control = None
        self.__pedido_control = None
        self.__restaurante_control = None

        self.__db_connection = None

    def init(self):
        MeuTokenJWT()
        self.__before_routing()

        self.__db_connection = MysqlDatabase(
            pool_name="pool_rh",
            pool_size=10,
            host="127.0.0.1",
            user="root",
            password="",
            database="delivery",
            port=3306
        )

        self.__db_connection.connect()

        self.__setup_funcionario()
        self.__setup_cliente()

        self.__setup_restaurante()
        self.__setup_pedido()

        self.__error_middleware()

    def __setup_funcionario(self):
        dao = FuncionarioDAO(self.__db_connection)
        service = FuncionarioService(dao)
        control = FuncionarioControl(service)
        router = FuncionarioRoteador(control)
        self.__app.register_blueprint(router.create_routes(), url_prefix="/api/v1/funcionarios")

    def __setup_cliente(self):
        print("⬆️  Setup Cliente:server")

        self.__cliente_dao = ClienteDAO(self.__db_connection)

        self.__cliente_service = ClienteService(self.__cliente_dao)

        self.__cliente_control = ClienteControl(self.__cliente_service)

        cliente_router = ClienteRoteador(
            self.__jwt_middleware,
            self.__cliente_middleware,
            self.__cliente_control
        )

        self.__app.register_blueprint(cliente_router.create_routes(), url_prefix="/api/v1/clientes")

    def __setup_pedido(self):
        print("⬆️  Setup Pedido:server")

        self.__pedido_dao = PedidoDAO(self.__db_connection)

        if self.__pedido_dao is None:
            self.__pedido_dao = PedidoDAO(self.__db_connection)

        self.__pedido_service = PedidoService(self.__pedido_dao, self.__cliente_dao, self.__restaurante_dao)

        self.__pedido_control = PedidoControl(self.__pedido_service)

        pedido_router = PedidoRoteador(
            self.__jwt_middleware,
            self.__pedido_middleware,
            self.__pedido_control
        )

        self.__app.register_blueprint(pedido_router.create_routes(), url_prefix="/api/v1/pedidos")
        
    def __setup_restaurante(self):
        print(" Setup Pedido:server")
        
        self.__restaurante_dao = RestauranteDAO(self.__db_connection)
        
        if self.__restaurante_dao is None:
            self.__restaurante_dao = RestauranteDAO(self.__db_connection)
            
        self.__restaurante_service = RestauranteService(self.__restaurante_dao)
        
        self.__restaurante_control = RestauranteControl(self.__restaurante_service)
        
        restaurante_router = RestauranteRoteador(
            self.__jwt_middleware,
            self.__restaurante_middleware,
            self.__restaurante_control
        )
        
        self.__app.register_blueprint(restaurante_router.create_routes(), url_prefix="/api/v1/restaurantes")

    def __before_routing(self):
        @self.__app.before_request
        def log_separator():
            print("-" * 70)

    def __error_middleware(self):
        @self.__app.errorhandler(Exception)
        def handle_error(error):
           

            if isinstance(error, NotFound):
                return error, 404

            if isinstance(error, ErrorResponse):
                print("🟡 Server.error_middleware()")
                stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))

                Logger.log_error(error)  

                resposta = {
                    "success": False,
                    "error": {
                        "message": str(error),
                        "code": getattr(error, "code", None),
                        "details": getattr(error, "error", None)
                    },
                    "data": {
                        "message": "Erro tratado pela aplicação",
                        "stack": stack_str
                    }
                }
                return jsonify(resposta), error.httpCode

            stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            print("🟡 Server.error_middleware()")
            resposta = {
                "success": False,
                "error": {
                    "message": str(error),
                    "code": getattr(error, "code", None)
                },
                "data": {
                    "message": "Ocorreu um erro interno no servidor",
                    "stack": stack_str
                }
            }

            Logger.log_error(error)  
            return jsonify(resposta), 500

    def run(self):
        print(f"🚀 Servidor rodando em: http://127.0.0.1:{self.__porta}/login.html")
        self.__app.run(port=self.__porta, debug=False)