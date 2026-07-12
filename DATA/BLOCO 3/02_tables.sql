CREATE TABLE Preco_Sazonal (
    id_preco INT AUTO_INCREMENT PRIMARY KEY,
    id_modulo INT NOT NULL,
    id_temporada INT NOT NULL,
    valor_sugerido DECIMAL(10, 2) NOT NULL,
    UNIQUE (id_modulo, id_temporada),
    FOREIGN KEY (id_modulo) REFERENCES Modulos_Pacote(id_modulo),
    FOREIGN KEY (id_temporada) REFERENCES Temporada(id_temporada)
);

CREATE TABLE Cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf_criptografado VARCHAR(255) UNIQUE,
    email_criptografado VARCHAR(255) UNIQUE,
    telefone_criptografado VARCHAR(255),
    cep VARCHAR(9),
    id_municipio_origem INT,
    FOREIGN KEY (id_municipio_origem) REFERENCES Municipio(id_municipio)
);

CREATE TABLE Interesses_Cliente (
    id_interesse INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_municipio_destino INT NOT NULL,
    status VARCHAR(50),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_municipio_destino) REFERENCES Municipio(id_municipio)
);

CREATE TABLE Oportunidade_CRM (
    id_oportunidade INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_usuario_interno INT,
    estagio_funil VARCHAR(50) NOT NULL,
    valor_estimado DECIMAL(10, 2),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_usuario_interno) REFERENCES Usuario_Interno(id_usuario_interno)
);

CREATE TABLE Historico_Interacoes (
    id_interacao INT AUTO_INCREMENT PRIMARY KEY,
    id_oportunidade INT NOT NULL,
    id_cliente INT,
    id_usuario_interno INT,
    tipo_interacao VARCHAR(50) NOT NULL,
    data_interacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_oportunidade) REFERENCES Oportunidade_CRM(id_oportunidade),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_usuario_interno) REFERENCES Usuario_Interno(id_usuario_interno)
);