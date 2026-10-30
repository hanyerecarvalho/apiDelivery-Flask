# -*- coding: utf-8 -*-
from api.model.Restaurantes import Restaurante

class RestaurantesDAO:
    def __init__(self, database_dependency):
        print("⬆️  RestaurantesDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objRestaurantes: Restaurante) -> int:
        SQL = "INSERT INTO restaurantes ( nomeRestaurante, telefoneRestaurante, enderecoRestaurante) VALUES (%s);"
        params = (objRestaurantes.nomeRestaurante,objRestaurantes.telefoneRestaurante, objRestaurantes.enderecoRestaurante)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir restaurante")
        print("✅ RestauranteDAO.create()")
        return insert_id

    def delete(self, restaurantes: Restaurante) -> bool:
        SQL = "DELETE FROM restaurantes WHERE idRestaurante = %s;"
        params = (restaurantes.idRestaurante,)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ RestauranteDAO.delete()")
        return affected > 0

    def update(self, objRestaurantes: Restaurante) -> bool:
        SQL = "UPDATE restaurantes SET nomeRestaurante, telefoneRestaurante, enderecoRestaurante = %s WHERE idRestaurante = %s;"
        params = (objRestaurantes.nomeRestaurante, objRestaurantes.telefoneRestaurante, objRestaurantes.enderecoRestaurante, objRestaurantes.idRestaurante)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ RestauranteDAO.update()")
        return affected > 0

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM restaurantes;"

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                resultados = cursor.fetchall()

        print(f"✅ RestauranteDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados

    def findById(self, idRestaurante: int) -> dict | None:
        resultados = self.findByField("idRestaurante", idRestaurante)
        print("✅ RestauranteDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idRestaurante", "nomeRestaurante", "telefoneRestaurante","enderecoRestaurante"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM restaurantes WHERE {field} = %s;"
        params = (value,)

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()

        print("✅ RestauranteDAO.findByField()")
        return resultados