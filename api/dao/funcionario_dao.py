from api.model.funcionario import Funcionario


class FuncionarioDAO:
    def __init__(self, database):
        self.__database = database

    def buscar_por_email(self, email):
        sql = "SELECT idFuncionario, nome, email, senha_hash FROM contas_acesso WHERE email = %s"
        with self.__database.get_connection() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(sql, (email,))
                registro = cursor.fetchone()
        return Funcionario(*registro) if registro else None
