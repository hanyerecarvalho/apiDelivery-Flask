from math import isfinite


class Pedidos:
    def __init__(self):
        self.__idPedidos = None
        self.__valorTotal = None
        self.__idCliente = None
        self.__idRestaurante = None

    @staticmethod
    def __validar_id(value, campo):
        if isinstance(value, bool) or not isinstance(value, (int, str)):
            raise ValueError(f"{campo} deve ser um inteiro positivo.")
        numero = int(value)
        if numero <= 0:
            raise ValueError(f"{campo} deve ser um inteiro positivo.")
        return numero

    @property
    def idPedido(self):
        return self.__idPedidos

    @idPedido.setter
    def idPedido(self, value):
        self.__idPedidos = self.__validar_id(value, "idPedido")

    @property
    def valorTotal(self):
        return self.__valorTotal

    @valorTotal.setter
    def valorTotal(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise ValueError("valorTotal deve ser um número positivo.")
        numero = float(value)
        if not isfinite(numero) or numero <= 0:
            raise ValueError("valorTotal deve ser um número positivo.")
        self.__valorTotal = numero

    @property
    def idCliente(self):
        return self.__idCliente

    @idCliente.setter
    def idCliente(self, value):
        self.__idCliente = self.__validar_id(value, "idCliente")

    @property
    def idRestaurante(self):
        return self.__idRestaurante

    @idRestaurante.setter
    def idRestaurante(self, value):
        self.__idRestaurante = self.__validar_id(value, "idRestaurante")
