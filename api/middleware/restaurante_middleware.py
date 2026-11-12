# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class RestauranteMiddleware:

    def validate_body(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 RestauranteMiddleware.validate_body()")
            body = request.get_json()
            
            if not body or 'restaurante' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'restaurante' é obrigatório!"})

            restaurante = body['restaurante']

            campos_obrigatorios = ["nomeRestaurante", "telefoneRestaurante", "enderecoRestaurante"]
            for campo in campos_obrigatorios:
                if campo not in restaurante:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 RestauranteMiddleware.validate_id_param()")
            if 'idRestaurante' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'idRestaurante' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function