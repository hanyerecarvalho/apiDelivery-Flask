from flask import request, jsonify
from api.service.restaurante_service import RestauranteService

class RestauranteControl:
    def __init__(self, restaurante_service:RestauranteService):
        print("⬆️  RestauranteControl.constructor()")
        self.__restaurante_service = restaurante_service

    def store(self):
        print("🔵 RestauranteControle.store()")
       
        restaurante_body_request = request.json.get("restaurante")
        novo_id = self.__restaurante_service.createRestaurante(restaurante_body_request)

        obj_resposta = {
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "restaurantes": [
                    {
                        "idRestaurante": novo_id,
                        "nomeRestaurante": restaurante_body_request.get("nomeRestaurante"),
                        "telefoneRestaurante": restaurante_body_request.get("telefoneRestaurante"),
                        "enderecoRestaurante": restaurante_body_request.get("enderecoRestaurante")
                    }
                ]
            }
        }

        if novo_id:
            return jsonify(obj_resposta), 200
        

    def index(self):
        print("🔵 RestauranteControle.index()")
       
        array_restaurantes = self.__restaurante_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {"restaurantes": array_restaurantes}
        }), 200
        

    def show(self):
        idRestaurante = request.view_args.get("idRestaurante")

        restaurante = self.__restaurante_service.findById(idRestaurante)
        obj_resposta = {
            "success": True,
            "message": "Executado com sucesso",
            "data": {"restaurantes": restaurante}
        }
        return jsonify(obj_resposta), 200
      

    def update(self):
        print("🔵 RestauranteControle.update()")
       
        # Pega o idCargo diretamente da URI
        idRestaurante = request.view_args.get("idRestaurante")

        # Pega os dados do cargo no corpo da requisição
        json_restaurante = request.json.get("restaurante")
        print(json_restaurante)

        resposta = self.__restaurante_service.updateRestaurante(idRestaurante, json_restaurante)
        return jsonify({

            "success": True,
            "message": "restaurante atualizado com sucesso",
            "data": {
                "restaurante": {
                    "idRestaurante": int(idRestaurante),
                    "nomeRestaurante": json_restaurante.get("nomeRestaurante"),
                    "telefoneRestaurante": json_restaurante.get("telefoneRestaurante"),
                    "enderecoRestaurante": json_restaurante.get("enderecoRestaurante")
                }
            }
        }), 200
   

    def destroy(self):
        print("🔵 RestauranteControle.destroy()")
        # Pega o idCargo diretamente da URI
        idRestaurante = request.view_args.get("idRestaurante")
        
        excluiu = self.__restaurante_service.deleteRestaurante(idRestaurante)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe cliente com id {idRestaurante}"
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 204
        