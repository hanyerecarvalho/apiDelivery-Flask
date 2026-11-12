USE delivery;
CREATE TABLE IF NOT EXISTS contas_acesso (
    idFuncionario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    senha_hash VARCHAR(161) NOT NULL
);
