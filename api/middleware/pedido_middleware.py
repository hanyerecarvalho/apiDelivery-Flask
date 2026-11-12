# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class PedidoMiddleware:

    def validate_body(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 PedidoMiddleware.validate_body()")
            body = request.get_json()
            
            if not body or 'pedido' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'pedido' é obrigatório!"})

            pedido = body['pedido']

            campos_obrigatorios = ["valorTotal", "idCliente", "idRestaurante"]
            for campo in campos_obrigatorios:
                if campo not in pedido:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 PedidoMiddleware.validate_id_param()")
            if 'idPedido' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'idPedido' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function