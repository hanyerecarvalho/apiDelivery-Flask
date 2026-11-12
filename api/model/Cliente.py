# -*- coding: utf-8 -*-

class Cliente:
    def __init__(self):
        self.__idCliente = None
        self.__nomeCliente = None
        self.__telefoneCliente = None

    @property
    def idCliente(self):

        return self.__idCliente

    @idCliente.setter
    def idCliente(self, value):
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("idCliente deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("idCliente deve ser maior que zero.")

        self.__idCliente = parsed

    @property
    def nomeCliente(self):

        return self.__nomeCliente

    @nomeCliente.setter
    def nomeCliente(self, value):
        if not isinstance(value, str):
            raise ValueError("nomeCliente deve ser uma string.")

        nome = value.strip()
        if len(nome) < 3:
            raise ValueError("nomeCliente deve ter pelo menos 3 caracteres.")

        self.__nomeCliente = nome

    @property
    def telefoneCliente(self):
        return self.__telefoneCliente

    @telefoneCliente.setter
    def telefoneCliente(self, value):
        if not isinstance(value, str):
            raise ValueError("telefoneCliente deve ser uma string")

        telefone = value.strip()
        if len(telefone) < 3:
            raise ValueError("telefoneCliente deve ter mais de 3 caracteres")

        self.__telefoneCliente = telefone