-- Active: 1782324666582@@mysql-luxevoyage-projetoluxevoyage.a.aivencloud.com@18410@LuxeVoyage
CREATE TABLE Avaliacoes_Parceiros (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    id_parceiro INT NOT NULL,
    id_usuario_interno INT,
    nota INT CHECK (nota >= 1 AND nota <= 5),
    comentarios TEXT,
    FOREIGN KEY (id_parceiro) REFERENCES Parceiros(id_parceiro),
    FOREIGN KEY (id_usuario_interno) REFERENCES Usuario_Interno(id_usuario_interno)
);

CREATE TABLE Destaques_Sazonais (
    id_destaque INT AUTO_INCREMENT PRIMARY KEY,
    id_municipio INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    classificacao VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_municipio) REFERENCES Municipio(id_municipio)
);

CREATE TABLE Pacote (
    id_pacote INT AUTO_INCREMENT PRIMARY KEY,
    nome_pacote VARCHAR(255) NOT NULL,
    id_municipio_destino INT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Rascunho',
    FOREIGN KEY (id_municipio_destino) REFERENCES Municipio(id_municipio)
);

CREATE TABLE Temporada (
    id_temporada INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL
);

CREATE TABLE Modulos_Pacote (
    id_modulo INT AUTO_INCREMENT PRIMARY KEY,
    id_pacote INT NOT NULL,
    id_servico_parceiro INT NOT NULL,
    obrigatorio BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (id_pacote, id_servico_parceiro),
    FOREIGN KEY (id_pacote) REFERENCES Pacote(id_pacote),
    FOREIGN KEY (id_servico_parceiro) REFERENCES Servicos_Parceiros(id_servico_parceiro)
);