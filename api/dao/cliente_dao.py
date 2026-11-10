# -*- coding: utf-8 -*-
from api.model.Cliente import Cliente

class ClienteDAO:
    def __init__(self, database_dependency):
        print("⬆️  ClienteDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objCliente: Cliente) -> int:
        SQL = "INSERT INTO clientes (nomeCliente, telefoneCliente) VALUES (%s);"
        params = (objCliente.nomeCliente,objCliente.telefoneCliente)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir cliente")
        print("✅ ClienteDAO.create()")
        return insert_id

    def delete(self, cliente: Cliente) -> bool:
        SQL = "DELETE FROM clientes WHERE idCliente = %s;"
        params = (cliente.idCliente,)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ ClienteDAO.delete()")
        return affected > 0

    def update(self, objCliente: Cliente) -> bool:
        SQL = "UPDATE clientes SET nomeCliente, telefoneCliente = %s WHERE idCliente = %s;"
        params = (objCliente.nomeCliente, objCliente.telefoneCliente, objCliente.idCliente)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ ClienteDAO.update()")
        return affected > 0

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM clientes;"

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                resultados = cursor.fetchall()

        print(f"✅ ClienteDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados

    def findById(self, idCliente: int) -> dict | None:
        resultados = self.findByField("idCliente", idCliente)
        print("✅ ClienteDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idCliente", "nomeCliente", "telefoneCliente"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM clientes WHERE {field} = %s;"
        params = (value,)

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()

        print("✅ ClienteDAO.findByField()")
        return resultados