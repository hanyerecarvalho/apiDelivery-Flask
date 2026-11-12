class Funcionario:
    def __init__(self, id_funcionario, nome, email, senha_hash):
        self.id_funcionario = id_funcionario
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
