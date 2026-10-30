# -*- coding: utf-8 -*-

class Restaurante:
    def __init__(self):
        self.__idRestaurante = None
        self.__nomeRestaurante = None
        self.__telefoneRestaurante = None
        self.__enderecoRestaurante = None

    @property
    def idRestaurante(self):

        return self.__idRestaurante

    @idRestaurante.setter
    def idRestaurante(self, value):
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("idRestaurante deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("idRestaurante deve ser maior que zero.")

        self.__idRestaurante = parsed

    @property
    def nomeRestaurante(self):

        return self.__nomeRestaurante

    @nomeRestaurante.setter
    def nomeRestaurante(self, value):
        if not isinstance(value, str):
            raise ValueError("nomeRestaurante deve ser uma string.")

        nome = value.strip()
        if len(nome) < 3:
            raise ValueError("nomeRestaurante deve ter pelo menos 3 caracteres.")

        self.__nomeRestaurante = nome

    @property
    def telefoneRestaurante(self):
        return self.__telefoneRestaurante

    @telefoneRestaurante.setter
    def telefoneRestaurante(self, value):
        if not isinstance(value, str):
            raise ValueError("telefoneRestaurante deve ser uma string")

        telefone = value.strip()
        if len(telefone) < 3:
            raise ValueError("telefoneRestaurante deve ter mais de 3 caracteres")

        self.__telefoneRestaurante = telefone

    @property
    def enderecoRestaurante(self):
        return self.__enderecoRestaurante

    @enderecoRestaurante.setter
    def enderecoRestaurante(self, value):
        if not isinstance(value, str):
            raise ValueError("enderecoRestaurante deve ser uma string")
        endereco = value.strip()
        if len(endereco) < 3:
            raise ValueError("enderecoRestaurante deve ter mais de 3 caracteres")

        self.__enderecoRestaurante = endereco