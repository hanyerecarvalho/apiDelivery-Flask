from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from werkzeug.exceptions import HTTPException, NotFound

from api.database.mysql_database import MysqlDatabase
from api.utils.error_response import ErrorResponse
from api.utils.logger import Logger

# Middlewares
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.cargo_middleware import CargoMiddleware
from api.middleware.funcionario_middleware import FuncionarioMiddleware

# Controls
from api.control.cargo_control import CargoControl
from api.control.funcionario_control import FuncionarioControl

# Services
from api.service.cargo_service import CargoService
from api.service.funcionario_service import FuncionarioService

# DAOs
from api.dao.cargo_dao import CargoDAO
from api.dao.funcionario_dao import FuncionarioDAO

# Routers
from api.router.cargo_roteador import CargoRoteador
from api.router.funcionario_roteador import FuncionarioRoteador

import traceback


class Server:
    """
    Classe principal do servidor Flask.

    Responsável por inicializar middlewares, roteadores e gerenciar a aplicação.
    """

    def __init__(self, porta: int = 8080):
        # 🔹 Porta em que o servidor irá rodar
        self.__porta = porta

        # 🔹 Instância Flask, configurando pasta de arquivos estáticos
        self.__app = Flask(__name__, static_folder="static", static_url_path="")

        # 🔹 Configuração de CORS (Cross-Origin Resource Sharing)
        #    Permite que clientes de outros domínios/portas acessem sua API
        #    Exemplo: permitir todos os domínios (somente para desenvolvimento)
        CORS(self.__app, resources={r"/*": {"origins": "*"}})

        # 🔹 Middlewares
        self.__jwt_middleware = JwtMiddleware()
        self.__cargo_middleware = CargoMiddleware()
        self.__funcionario_middleware = FuncionarioMiddleware()

        # 🔹 DAOs, Services e Controls serão inicializados após conexão com DB
        self.__cargo_dao = None
        self.__funcionario_dao = None
        self.__cargo_service = None
        self.__funcionario_service = None
        self.__cargo_control = None
        self.__funcionario_control = None

        # 🔹 Conexão global com o banco
        self.__db_connection = None

    def init(self):
        """
        Inicializa a aplicação:
        - Conexão com o banco
        - Middlewares
        - Roteadores
        """
        # Middleware para parsing JSON já é nativo do Flask
        # Middleware para arquivos estáticos já configurado na criação do Flask

        # 🔹 Middleware de log antes das rotas
        self.__before_routing()

        # 🔹 Conexão global com MySQL (injeção de dependência)
        self.__db_connection = MysqlDatabase(
            pool_name="pool_rh",
            pool_size=10,
            host="127.0.0.1",
            user="root",
            password="",
            database="gestao_rh",
            port=3306
        )

        self.__db_connection.connect()

        # 🔹 Configuração do módulo Cargo
        self.__setup_cargo()

        # 🔹 Configuração do módulo Funcionario
        self.__setup_funcionario()

        # 🔹 Middleware global de tratamento de erros
        self.__error_middleware()

    def __setup_cargo(self):
        """Configura o módulo Cargo (DAO, Service, Control, Router)"""
        print("⬆️  Setup Cargo")

        # DAO recebe conexão global com o banco (injeção de dependência)
        self.__cargo_dao = CargoDAO(self.__db_connection)

        # Service recebe DAO (injeção de dependência)
        self.__cargo_service = CargoService(self.__cargo_dao)

        # Controller recebe Service (injeção de dependência)
        self.__cargo_control = CargoControl(self.__cargo_service)

        # Router recebe Controller + Middlewares
        cargo_router = CargoRoteador(
            self.__jwt_middleware,
            self.__cargo_middleware,
            self.__cargo_control
        )

        # Registra rotas da entidade Cargo
        self.__app.register_blueprint(cargo_router.create_routes(), url_prefix="/api/v1/cargos")

    def __setup_funcionario(self):
        """Configura o módulo Funcionario (DAO, Service, Control, Router)"""
        print("⬆️  Setup Funcionário")

        # DAO recebe conexão global com o banco (injeção de dependência)
        self.__funcionario_dao = FuncionarioDAO(self.__db_connection)

        # 🔹 Garante que CargoDAO existe (dependência cruzada)
        if self.__cargo_dao is None:
            self.__cargo_dao = CargoDAO(self.__db_connection)

        # Service recebe DAOs via injeção de dependência
        self.__funcionario_service = FuncionarioService(self.__funcionario_dao, self.__cargo_dao)

        # Controller recebe Service
        self.__funcionario_control = FuncionarioControl(self.__funcionario_service)

        # Router recebe Controller + Middlewares
        funcionario_router = FuncionarioRoteador(
            self.__jwt_middleware,
            self.__funcionario_middleware,
            self.__funcionario_control
        )

        # Registra rotas da entidade Funcionário
        self.__app.register_blueprint(funcionario_router.create_routes(), url_prefix="/api/v1/funcionarios")

    def __before_routing(self):
        """Middleware que loga separador antes de cada requisição"""
        @self.__app.before_request
        def log_separator():
            print("-" * 70)

    def __error_middleware(self):
        """Middleware global de tratamento de erros"""
        @self.__app.errorhandler(Exception)
        def handle_error(error):
           

            # 🔹 404 - Rota ou arquivo não encontrado
            if isinstance(error, NotFound):
                return error, 404

            # 🔹 Captura ErrorResponse customizado
            if isinstance(error, ErrorResponse):
                print("🟡 Server.error_middleware()")
                # Extrai stack trace como string
                stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))

                Logger.log_error(error)  # Loga a exceção real

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

            # 🔹 Outros erros internos (não tratados)
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

            Logger.log_error(error)  # Loga a exceção real
            return jsonify(resposta), 500

    def run(self):
        """Inicia o servidor Flask na porta configurada"""
        print(f"🚀 Servidor rodando em: http://127.0.0.1:{self.__porta}/Login.html")
        # ⚠️ debug=False é necessário para que o errorhandler global capture exceções
        self.__app.run(port=self.__porta, debug=False)