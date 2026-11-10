# -*- coding: utf-8 -*-
from api.dao.cliente_dao import ClienteDAO
from api.model.Cliente import Cliente
from api.utils.error_response import ErrorResponse

class ClienteService:
    def __init__(self, cliente_dao_dependency: ClienteDAO):

        print("⬆️  ClienteService.__init__()")
        self.__clienteDAO = cliente_dao_dependency 

    def createCliente(self, clienteBodyRequest: dict) -> int:
        print("🟣 ClienteService.createCliente()")

        cliente = Cliente()
        cliente.nomeCliente = clienteBodyRequest.get("nomeCliente")
        cliente.telefoneCliente = clienteBodyRequest.get("telefoneCliente")

        # valida regra de negócio: Cliente duplicado
        resultado = self.__clienteDAO.findByField("telefoneCliente", cliente.telefoneCliente)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Cliente já existe",
                {"message": f"O cliente {cliente.telefoneCliente} já existe"}
            )

        return  self.__clienteDAO.create(cliente)

    def findAll(self) -> list[dict]:
        print("🟣 ClienteService.findAll()")
        return self.__clienteDAO.findAll()

    def findById(self, idCliente: int) -> dict | None:
        print("🟣 ClienteService.findById()")

        cliente = Cliente()
        cliente.idCliente = idCliente  # passa pela validação de domínio

        return self.__clienteDAO.findById(cliente.idCliente)

    def updateCliente(self, idCliente: int, jsonCliente: dict) -> bool:
        print (jsonCliente)
        print("🟣 ClienteService.updateCliente()")

        cliente = Cliente()
        cliente.idCliente = idCliente
        cliente.nomeCliente = jsonCliente.get("nomeCliente")
        cliente.telefoneCliente = jsonCliente.get("telefoneCliente")

        return self.__clienteDAO.update(cliente)

    def deleteCliente(self, idCliente: int) -> bool:
        print("🟣 ClienteService.deleteCliente()")

        cliente = Cliente()
        cliente.idCliente = idCliente  # validação de regra de domínio

        return self.__clienteDAO.delete(cliente)