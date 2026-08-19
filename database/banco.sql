CREATE DATABASE IF NOT EXISTS oficina_mecanica
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE oficina_mecanica;

CREATE TABLE IF NOT EXISTS cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(45),
    telefone VARCHAR(45),
    `endereço` VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS veiculo_cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(45),
    cor VARCHAR(45),
    ano VARCHAR(45),
    problema_apresentado VARCHAR(150),
    dono_veiculo INT,
    placa_veiculo VARCHAR(45),
    CONSTRAINT fk_veiculo_cliente
        FOREIGN KEY (dono_veiculo) REFERENCES cliente(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS equipe_mecanico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(45),
    `endereço` VARCHAR(45),
    especialidade VARCHAR(45),
    codigo_mecanico INT UNIQUE
);

CREATE TABLE IF NOT EXISTS `tabela_peças` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `valor_peça` FLOAT,
    tempo_garantia VARCHAR(45),
    `nome_peça` VARCHAR(45),
    `descriçao` VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS mao_de_obra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    valor INT,
    `descriçao` VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS `ordem_de_serviço` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_emissao DATE,
    valor INT,
    status VARCHAR(45),
    data_conclusao VARCHAR(45),
    ordem_veiculo INT,
    ordem_mecanico INT,
    CONSTRAINT fk_os_veiculo
        FOREIGN KEY (ordem_veiculo) REFERENCES veiculo_cliente(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_os_mecanico
        FOREIGN KEY (ordem_mecanico) REFERENCES equipe_mecanico(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `serviços` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `serviços_solicitados` VARCHAR(45),
    mao_de_obra_do_serviço INT,
    CONSTRAINT fk_servico_mao_obra
        FOREIGN KEY (mao_de_obra_do_serviço) REFERENCES mao_de_obra(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `serviços_os` (
    id_serviços INT,
    id_ordem INT,
    PRIMARY KEY (id_serviços, id_ordem),
    CONSTRAINT fk_servicos_os_servico
        FOREIGN KEY (id_serviços) REFERENCES `serviços`(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_servicos_os_ordem
        FOREIGN KEY (id_ordem) REFERENCES `ordem_de_serviço`(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `peças_na_os` (
    id_peças INT,
    id_ordem INT,
    PRIMARY KEY (id_peças, id_ordem),
    CONSTRAINT fk_pecas_os_peca
        FOREIGN KEY (id_peças) REFERENCES `tabela_peças`(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_pecas_os_ordem
        FOREIGN KEY (id_ordem) REFERENCES `ordem_de_serviço`(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
