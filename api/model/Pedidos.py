# -*- coding: utf-8 -*-

class Pedidos:
    def __init__(self):
        self.__idPedidos = None
        self.__valorTotal = None
        self.__idCliente = None
        self.__idRestaurante = None

    @property
    def idPedido(self):

        return self.__idPedidos

    @idPedido.setter
    def idPedido(self, value):
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("idPedido deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("idPedido deve ser maior que zero.")

        self.__idRestaurante = parsed

    @property
    def valorTotal(self):

        return self.__valorTotal

    @valorTotal.setter
    def valorTotal(self, value):
        if not isinstance(value, str):
            raise ValueError("valorTotal deve ser uma string.")

        valorTotal = value.strip()
        if len(valorTotal) < 3:
            raise ValueError("valorTotal deve ter pelo menos 3 caracteres.")

        self.__valorTotal = valorTotal

    @property
    def idCliente(self):
        return self.__idCliente

    @idCliente.setter
    def idCliente(self, value):
        if not isinstance(value, str):
            raise ValueError("idCliente deve ser uma string")

        idCliente = value.strip()
        if len(idCliente) < 3:
            raise ValueError("idCliente deve ter mais de 3 caracteres")

        self.__idCliente = idCliente

    @property
    def idRestaurante(self):
        return self.__idRestaurante

    @idRestaurante.setter
    def idRestaurante(self, value):
        if not isinstance(value, str):
            raise ValueError("idRestaurante deve ser uma string")
        idRestaurante = value.strip()
        if len(idRestaurante) < 3:
            raise ValueError("idRestaurante deve ter mais de 3 caracteres")

        self.__idRestaurante = idRestaurante