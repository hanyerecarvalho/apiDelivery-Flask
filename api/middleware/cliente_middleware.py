# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class ClienteMiddleware:

    def validate_create_body(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ClienteMiddleware.validate_create_body()")
            body = request.get_json()
            
            if not body or 'cliente' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'cliente' é obrigatório!"})

            cliente = body['cliente']

            campos_obrigatorios = ["nomeCliente", "telefoneCliente"]
            for campo in campos_obrigatorios:
                if campo not in cliente:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ClienteMiddleware.validate_id_param()")
            if 'idCliente' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'idCliente' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function