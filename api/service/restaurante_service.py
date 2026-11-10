# -*- coding: utf-8 -*-
from api.dao.restaurante_dao import RestauranteDAO
from api.model.Restaurantes import Restaurante
from api.utils.error_response import ErrorResponse

class RestauranteService:
    def __init__(self, restaurante_dao_dependency: RestauranteDAO):

        print("⬆️  RestauranteService.__init__()")
        self.__restauranteDAO = restaurante_dao_dependency 

    def createRestaurante(self, restauranteBodyRequest: dict) -> int:
        print("🟣 RestauranteService.createRestaurante()")

        restaurante = Restaurante()
        restaurante.nomeRestaurante = restauranteBodyRequest.get("nomeRestaurante")
        restaurante.telefoneRestaurante = restauranteBodyRequest.get("telefoneRestaurante")
        restaurante.enderecoRestaurante = restauranteBodyRequest.get("enderecoRestaurante")

        # valida regra de negócio: restaurante duplicado
        resultado = self.__restauranteDAO.findByField("nomeRestaurante", restaurante.nomeRestaurante)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Restaurante já existe",
                {"message": f"O restaurante {restaurante.nomeRestaurante} já existe"}
            )
        resultado = self.__restauranteDAO.findByField("telefoneRestaurante", restaurante.telefoneRestaurante)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Restaurante ja existe",
                {"message": f"o restaurante {restaurante.telefoneRestaurante} ja existe"}
            )
        resultado = self.__restauranteDAO.findByField("enderecoRestaurante", restaurante.enderecoRestaurante)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Restaurante ja existe",
                {"message": f"o restaurante {restaurante.enderecoRestaurante} ja existe"}
            )

        return  self.__restauranteDAO.create(restaurante)

    def findAll(self) -> list[dict]:
        print("🟣 RestauranteService.findAll()")
        return self.__restauranteDAO.findAll()

    def findById(self, idRestaurante: int) -> dict | None:
        print("🟣 RestauranteService.findById()")

        restaurante = Restaurante()
        restaurante.idRestaurante = idRestaurante  # passa pela validação de domínio

        return self.__restauranteDAO.findById(restaurante.idRestaurante)

    def updateRestaurante(self, idRestaurante: int, jsonRestaurante: dict) -> bool:
        print (jsonRestaurante)
        print("🟣 RestauranteService.updateRestaurante()")

        restaurante = Restaurante()
        restaurante.idRestaurante = idRestaurante
        restaurante.nomeRestaurante = jsonRestaurante.get("nomeRestaurante")
        restaurante.telefoneRestaurante = jsonRestaurante.get("telefoneRestaurante")
        restaurante.enderecoRestaurante = jsonRestaurante.get("enderecoRestaurante")

        return self.__restauranteDAO.update(restaurante)

    def deleteRestaurante(self, idRestaurante: int) -> bool:
        print("🟣 RestauranteService.deleteRestaurante()")

        restaurante = Restaurante()
        restaurante.idRestaurante = idRestaurante  # validação de regra de domínio

        return self.__restauranteDAO.delete(restaurante)