from flask import request, jsonify
from api.service.cliente_service import ClienteService

class ClienteControl:
    def __init__(self, cliente_service:ClienteService):
        print("⬆️  ClienteControl.constructor()")
        self.__cliente_service = cliente_service

    def store(self):
        print("🔵 ClienteControle.store()")
       
        cliente_body_request = request.json.get("cliente")
        novo_id = self.__cliente_service.createCliente(cliente_body_request)

        obj_resposta = {
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "clientes": [
                    {
                        "idCliente": novo_id,
                        "nomeCliente": cliente_body_request.get("nomeCliente"),
                        "telefoneCliente": cliente_body_request.get("telefoneCliente")
                    }
                ]
            }
        }

        if novo_id:
            return jsonify(obj_resposta), 200
        

    def index(self):
        print("🔵 ClienteControle.index()")
       
        array_clientes = self.__cliente_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {"clientes": array_clientes}
        }), 200
        

    def show(self):
        idCliente = request.view_args.get("idCliente")

        cliente = self.__cliente_service.findById(idCliente)
        obj_resposta = {
            "success": True,
            "message": "Executado com sucesso",
            "data": {"clientes": cliente}
        }
        return jsonify(obj_resposta), 200
      

    def update(self):
        print("🔵 ClienteControle.update()")
       
        # Pega o idCargo diretamente da URI
        idCliente = request.view_args.get("idCliente")

        # Pega os dados do cargo no corpo da requisição
        json_cliente = request.json.get("cliente")
        print(json_cliente)

        resposta = self.__cliente_service.updateCliente(idCliente, json_cliente)
        return jsonify({

            "success": True,
            "message": "Cliente atualizado com sucesso",
            "data": {
                "cliente": {
                    "idCliente": int(idCliente),
                    "nomeCliente": json_cliente.get("nomeCliente"),
                    "telefoneCliente": json_cliente.get("telefoneCliente")
                }
            }
        }), 200
   

    def destroy(self):
        print("🔵 ClienteControle.destroy()")
        # Pega o idCargo diretamente da URI
        idCliente = request.view_args.get("idCliente")
        
        excluiu = self.__cliente_service.deleteCliente(idCliente)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe cliente com id {idCliente}"
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 200
        
