CREATE TABLE Estado (
    id_estado INT AUTO_INCREMENT PRIMARY KEY,
    sigla VARCHAR(2) NOT NULL UNIQUE,
    nome VARCHAR(50) NOT NULL,
    regiao_nome VARCHAR(50) NOT NULL,
    timezone VARCHAR(50) NOT NULL
);

CREATE TABLE Municipio (
    id_municipio INT AUTO_INCREMENT PRIMARY KEY,
    id_estado INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    FOREIGN KEY (id_estado) REFERENCES Estado(id_estado)
);

CREATE TABLE Parceiros (
    id_parceiro INT AUTO_INCREMENT PRIMARY KEY,
    razao_social VARCHAR(255) NOT NULL,
    tipo_parceiro VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Ativo'
);

CREATE TABLE Cobertura_Parceiros (
    id_cobertura INT AUTO_INCREMENT PRIMARY KEY,
    id_parceiro INT NOT NULL,
    id_municipio INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Ativo',
    UNIQUE (id_parceiro, id_municipio),
    FOREIGN KEY (id_parceiro) REFERENCES Parceiros(id_parceiro),
    FOREIGN KEY (id_municipio) REFERENCES Municipio(id_municipio)
);

CREATE TABLE Servicos_Parceiros (
    id_servico_parceiro INT AUTO_INCREMENT PRIMARY KEY,
    id_parceiro INT NOT NULL,
    categoria_servico VARCHAR(50) NOT NULL,
    nome_servico VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_parceiro) REFERENCES Parceiros(id_parceiro)
);

CREATE TABLE Usuario_Interno (
    id_usuario_interno INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    email_corporativo VARCHAR(255) NOT NULL UNIQUE,
    nivel_acesso VARCHAR(50) NOT NULL
);
