# -*- coding: utf-8 -*-
from api.model.Pedidos import Pedidos

class PedidosDAO:
    def __init__(self, database_dependency):
        print("⬆️  PedidosDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objPedidos: Pedidos) -> int:
        SQL = "INSERT INTO pedidos ( valorTotal, idCliente, idRestaurante) VALUES (%s);"
        params = (objPedidos.valorTotal,objPedidos.idCliente, objPedidos.idRestaurante)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir pedido")
        print("✅ PedidoDAO.create()")
        return insert_id

    def delete(self, pedidos: Pedidos) -> bool:
        SQL = "DELETE FROM pedidos WHERE idPedido = %s;"
        params = (pedidos.idPedido,)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ PedidosDAO.delete()")
        return affected > 0

    def update(self, objPedidos: Pedidos) -> bool:
        SQL = "UPDATE pedidos SET valorTotal, idCliente, idRestaurante = %s WHERE idPedido = %s;"
        params = (objPedidos.valorTotal, objPedidos.idCliente, objPedidos.idRestaurante, objPedidos.idPedido)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ PedidosDAO.update()")
        return affected > 0

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM pedidos;"

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                resultados = cursor.fetchall()

        print(f"✅ PedidosDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados

    def findById(self, idPedido: int) -> dict | None:
        resultados = self.findByField("idPedido", idPedido)
        print("✅ PedidosDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idPedido", "valorTotal", "idCliente","idRestaurante"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM pedidos WHERE {field} = %s;"
        params = (value,)

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()

        print("✅ PedidosDAO.findByField()")
        return resultados