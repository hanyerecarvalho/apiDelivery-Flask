from flask import request, jsonify
from api.service.pedido_service import PedidoService

class PedidoControl:
    def __init__(self, pedido_service:PedidoService):
        print("⬆️  PedidoControl.constructor()")
        self.__pedido_service = pedido_service

    def store(self):
        print("🔵 PedidoControle.store()")
       
        pedido_body_request = request.json.get("pedido")
        novo_id = self.__pedido_service.createPedido(pedido_body_request)

        obj_resposta = {
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "pedidos": [
                    {
                        "idPedido": novo_id,
                        "valorTotal": pedido_body_request.get("valorTotal"),
                        "idCliente": pedido_body_request.get("idCliente"),
                        "idRestaurante": pedido_body_request.get("idRestaurante")
                    }
                ]
            }
        }

        if novo_id:
            return jsonify(obj_resposta), 200
        

    def index(self):
        print("🔵 PedidoControle.index()")
       
        array_pedidos = self.__pedido_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {"pedidos": array_pedidos}
        }), 200
        

    def show(self):
        idPedido = request.view_args.get("idPedido")

        pedido = self.__pedido_service.findById(idPedido)
        obj_resposta = {
            "success": True,
            "message": "Executado com sucesso",
            "data": {"pedidos": pedido}
        }
        return jsonify(obj_resposta), 200
      

    def update(self):
        print("🔵 PedidoControle.update()")
       
        # Pega o idCargo diretamente da URI
        idPedido = request.view_args.get("idPedido")

        # Pega os dados do cargo no corpo da requisição
        json_pedido = request.json.get("pedido")
        print(json_pedido)

        resposta = self.__pedido_service.updatePedido(idPedido, json_pedido)
        return jsonify({

            "success": True,
            "message": "Pedido atualizado com sucesso",
            "data": {
                "pedido": {
                    "idPedido": int(idPedido),
                    "valorTotal": json_pedido.get("valorTotal"),
                    "idCliente": json_pedido.get("idCliente"),
                    "idRestaurante": json_pedido.get("idRestaurante")
                }
            }
        }), 200
   

    def destroy(self):
        print("🔵 PedidoControle.destroy()")
        # Pega o idCargo diretamente da URI
        idPedido = request.view_args.get("idPedido")
        
        excluiu = self.__pedido_service.deletePedido(idPedido)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe cliente com id {idPedido}"
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 204
        