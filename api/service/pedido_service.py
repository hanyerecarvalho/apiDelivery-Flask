# -*- coding: utf-8 -*-
from api.dao.pedido_dao import PedidoDAO
from api.model.Pedidos import Pedidos
from api.utils.error_response import ErrorResponse

class PedidoService:
    def __init__(self, pedido_dao_dependency: PedidoDAO):

        print("⬆️  PedidoService.__init__()")
        self.__pedidoDAO = pedido_dao_dependency 

    def createPedido(self, pedidoBodyRequest: dict) -> int:
        print("🟣 PedidoService.createPedido()")

        pedido = Pedidos()
        pedido.valorTotal = pedidoBodyRequest.get("valorTotal")
        pedido.idCliente = pedidoBodyRequest.get("idCliente")
        pedido.idRestaurante = pedidoBodyRequest.get("idRestaurante")

        return  self.__pedidoDAO.create(pedido)

    def findAll(self) -> list[dict]:
        print("🟣 PedidoService.findAll()")
        return self.__pedidoDAO.findAll()

    def findById(self, idPedido: int) -> dict | None:
        print("🟣 PedidoService.findById()")

        pedido = Pedidos()
        pedido.idPedido = idPedido  # passa pela validação de domínio

        return self.__pedidoDAO.findById(pedido.idPedido)

    def updatePedido(self, idPedido: int, jsonPedido: dict) -> bool:
        print (jsonPedido)
        print("🟣 PedidoService.updatePedido()")

        pedido = Pedidos()
        pedido.idPedido = idPedido
        pedido.valorTotal = jsonPedido.get("valorTotal")
        pedido.idCliente = jsonPedido.get("idCliente")
        pedido.idRestaurante = jsonPedido.get("idRestaurante")

        return self.__pedidoDAO.update(pedido)

    def deletePedido(self, idPedido: int) -> bool:
        print("🟣 PedidoService.deletePedido()")

        pedido = Pedidos()
        pedido.idPedido = idPedido  # validação de regra de domínio

        return self.__pedidoDAO.delete(pedido)