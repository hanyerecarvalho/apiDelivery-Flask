# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class ClienteMiddleware:

    def validate_body(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ClienteMiddleware.validate_body()")
            body = request.get_json()

            if not body or 'cliente' not in body:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'cliente' é obrigatório!"}
                )

            cliente = body['cliente']
            if 'nomeCliente' not in cliente:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'nomeCliente' é obrigatório!"}
                )
            if 'telefoneCliente' not in cliente:
                raise ErrorResponse(
                    400, "Erro na validacao de dados",
                    {"message": "O campo 'telefoneCliente' e obrigatorio"}
                )

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ClienteMiddleware.validate_id_param()")
            if 'idCliente' not in kwargs:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O parâmetro 'idCliente' é obrigatório!"}
                )
            return f(*args, **kwargs)
        return decorated_function