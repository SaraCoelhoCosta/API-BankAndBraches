-- -----------------------------------------------------
-- Schema AgenciaBancaria
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `AgenciaBancaria`;
USE `AgenciaBancaria`;

-- -----------------------------------------------------
-- Criando tabela `cidades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cidades` (
  `id` INT NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = innodb;

-- -----------------------------------------------------
-- Criando tabela `agencias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agencias` (
  `id` INT NOT NULL,
  `descricao` VARCHAR(50) NULL,
  `sede` VARCHAR(45) NOT NULL,
  `cidades_id` INT NOT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = innodb;

-- -----------------------------------------------------
-- Criando tabela `contas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `contas` (
  `id` INT NOT NULL,
  `agencias_id` INT NOT NULL,
  `tipo_conta` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = innodb;

-- -----------------------------------------------------
-- Criando tabela `clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` INT NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `endereco` VARCHAR(100) NOT NULL,
  `cep` VARCHAR(9) NOT NULL,
  `telefone` VARCHAR(15) NOT NULL,
  `descricao` VARCHAR(50) NULL,
  PRIMARY KEY (`id`)
)
ENGINE = innodb;

-- -----------------------------------------------------
-- Criando tabela `clientes_has_contas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clientes_has_contas` (
  `clientes_id` INT NOT NULL,
  `contas_id` INT NOT NULL,
  PRIMARY KEY (`clientes_id`, `contas_id`)
)
ENGINE = innodb;


-- -----------------------------------------------------
-- Alterando tabelas e colocando chave estrangeira
-- -----------------------------------------------------
ALTER TABLE `agencias` ADD CONSTRAINT `fk_cidades` FOREIGN KEY ( `cidades_id` ) REFERENCES `cidades` ( `id` );
ALTER TABLE `contas` ADD CONSTRAINT `fk_agencias` FOREIGN KEY ( `agencias_id` ) REFERENCES `agencias` ( `id` );
ALTER TABLE `clientes_has_contas` ADD CONSTRAINT `fk_clientes` FOREIGN KEY ( `clientes_id` ) REFERENCES `clientes` ( `id` );
ALTER TABLE `clientes_has_contas` ADD CONSTRAINT `fk_contas` FOREIGN KEY ( `contas_id` ) REFERENCES `contas` ( `id` );

-- -----------------------------------------------------
-- Populando o BD
-- -----------------------------------------------------
INSERT INTO cidades (id, nome) VALUES
(1, 'Jequié'),
(2, 'Jitaúna'),
(3, 'Jaguaquara'),
(4, 'Ipiaú'),
(5, 'São Paulo'),
(6, 'Valença'),
(7, 'Ibirataia'),
(8, 'Salvador'),
(9, 'Vitória da Conquista'),
(10, 'Feira de Santana');

INSERT INTO agencias (id, descricao, sede, cidades_id) VALUES
(1, 'Banco do Brasil', 'São Paulo', 1),
(2, 'Itaú Unibanco', 'Rio de Janeiro', 2),
(3, 'Caixa Econômica Federal', 'Belo Horizonte', 3),
(4, 'Bradesco', 'Curitiba', 4),
(5, 'Santander', 'Porto Alegre', 5),
(6, 'Banco Inter', 'Brasília', 6),
(7, 'Banco do Nordeste', 'Salvador', 7),
(8, 'Banco do Estado do Rio Grande do Sul', 'Fortaleza', 8),
(9, 'Banco Safra', 'Recife', 9),
(10, 'Banco Pan', 'Manaus', 10);

INSERT INTO contas (id, agencias_id, tipo_conta) VALUES
(1, 1, 'Corrente'),
(2, 2, 'Poupança'),
(3, 3, 'Vale-refeição'),
(4, 4, 'Salário'),
(5, 5, 'Universitária'),
(6, 6, 'Internacional'),
(7, 7, 'Corrente'),
(8, 8, 'Poupança'),
(9, 9, 'Salário'),
(10, 10, 'Corrente');

INSERT INTO clientes (id, nome, endereco, cep, telefone, descricao) VALUES
(1, 'Lara Fábian', 'Rua ABC', '45200-000', '(73) 91234-5678', ''),
(2, 'Sara Coelho', 'Rua ABC', '45200-000', '(73) 91234-5671', ''),
(3, 'João Benevides', 'Rua ABC', '45200-000', '(73) 91234-5672', ''),
(4, 'William Jefferson', 'Rua ABC', '45200-000', '(73) 91234-5673', ''),
(5, 'Eduardo Machado', 'Rua ABC', '45200-000', '(73) 91234-5674', ''),
(6, 'Willian Dias', 'Rua ABC', '45200-000', '(73) 91234-5675', ''),
(7, 'Ana Carla', 'Rua ABC', '45200-000', '(73) 91234-5676', ''),
(8, 'Diego Oliveira', 'Rua ABC', '45200-000', '(73) 91234-5677', ''),
(9, 'Luan Evangelista', 'Rua ABC', '45200-000', '(73) 91234-5679', ''),
(10, 'Isabella Andrade', 'Rua ABC', '45200-000', '(73) 91234-5670', '');

INSERT INTO clientes_has_contas (clientes_id, contas_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);