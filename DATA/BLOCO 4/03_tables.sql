CREATE TABLE Solicitacao_SLA (
    id_solicitacao INT AUTO_INCREMENT PRIMARY KEY,
    id_oportunidade INT NOT NULL,
    id_parceiro INT NOT NULL,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_oportunidade) REFERENCES Oportunidade_CRM(id_oportunidade),
    FOREIGN KEY (id_parceiro) REFERENCES Parceiros(id_parceiro)
);

CREATE TABLE Cotacao_Personalizadas (
    id_cotacao INT AUTO_INCREMENT PRIMARY KEY,
    id_oportunidade INT NOT NULL,
    id_pacote INT,
    valor_total_calculado DECIMAL(10, 2),
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_oportunidade) REFERENCES Oportunidade_CRM(id_oportunidade),
    FOREIGN KEY (id_pacote) REFERENCES Pacote(id_pacote)
);

CREATE TABLE Item_Cotacao (
    id_item_cotacao INT AUTO_INCREMENT PRIMARY KEY,
    id_cotacao INT NOT NULL,
    id_modulo INT NOT NULL,
    valor_aplicado DECIMAL(10, 2) NOT NULL,
    UNIQUE (id_cotacao, id_modulo),
    FOREIGN KEY (id_cotacao) REFERENCES Cotacao_Personalizadas(id_cotacao),
    FOREIGN KEY (id_modulo) REFERENCES Modulos_Pacote(id_modulo)
);

CREATE TABLE Propostas_Comerciais (
    id_proposta INT AUTO_INCREMENT PRIMARY KEY,
    id_cotacao INT NOT NULL,
    versao INT NOT NULL DEFAULT 1,
    status VARCHAR(50) NOT NULL,
    UNIQUE (id_cotacao, versao),
    FOREIGN KEY (id_cotacao) REFERENCES Cotacao_Personalizadas(id_cotacao)
);

CREATE TABLE Contrato_Digital (
    id_contrato INT AUTO_INCREMENT PRIMARY KEY,
    id_proposta INT NOT NULL UNIQUE,
    timestamp_aceite TIMESTAMP NOT NULL,
    ip_aceite VARCHAR(45) NOT NULL,
    hash_integridade VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Assinado',
    FOREIGN KEY (id_proposta) REFERENCES Propostas_Comerciais(id_proposta)
);

CREATE TABLE Viagem (
    id_viagem INT AUTO_INCREMENT PRIMARY KEY,
    id_contrato INT NOT NULL UNIQUE,
    data_embarque TIMESTAMP NOT NULL,
    data_retorno TIMESTAMP NOT NULL,
    status_viagem VARCHAR(50) NOT NULL DEFAULT 'Confirmada',
    FOREIGN KEY (id_contrato) REFERENCES Contrato_Digital(id_contrato)
);


CREATE TABLE Pagamento_Contrato (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_contrato INT NOT NULL,
    metodo_pagamento VARCHAR(50) NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    numero_parcela INT NOT NULL DEFAULT 1, 
    total_parcelas INT NOT NULL DEFAULT 1,
    status_transacao VARCHAR(50) NOT NULL DEFAULT 'Pendente',
    FOREIGN KEY (id_contrato) REFERENCES Contrato_Digital(id_contrato)
);

CREATE TABLE Consentimentos_LGPD (
    id_consentimento INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    tipo_consentimento VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Ativo',
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);

CREATE TABLE Log_Acesso (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario_interno INT NOT NULL,
    id_cliente INT,
    tipo_operacao VARCHAR(50) NOT NULL,
    data_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario_interno) REFERENCES Usuario_Interno(id_usuario_interno),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);