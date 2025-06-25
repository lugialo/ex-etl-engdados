CREATE TABLE agendamento (
  id_agendamento SERIAL PRIMARY KEY,
  data_agendamento timestamp DEFAULT NULL,
  status_agendamento varchar(100) DEFAULT NULL,
  paciente_id_paciente int NOT NULL,
  odontologista_id_odontologista int NOT NULL
);

CREATE TABLE consulta (
  id_consulta SERIAL PRIMARY KEY,
  data_hora timestamp DEFAULT NULL,
  diagnostico text,
  tratamento text,
  agendamento_id_agendamento int NOT NULL
);

CREATE TABLE consulta_procedimento (
  id_consulta_procedimento SERIAL,
  consulta_id_consulta int NOT NULL,
  procedimento_id_procedimento int NOT NULL,
  PRIMARY KEY (id_consulta_procedimento, consulta_id_consulta, procedimento_id_procedimento)
);

CREATE TABLE endereco (
  id_endereco SERIAL PRIMARY KEY,
  logradouro varchar(255) NOT NULL,
  numero varchar(20) DEFAULT NULL,
  complemento varchar(100) DEFAULT NULL,
  bairro varchar(100) NOT NULL,
  cidade varchar(100) NOT NULL,
  estado char(2) NOT NULL,
  cep varchar(9) NOT NULL,
  pais varchar(200) NOT NULL
);

CREATE TABLE log_pagamento (
  id_log SERIAL PRIMARY KEY,
  tipo_acao varchar(10) NOT NULL,
  id_pagamento int NOT NULL,
  tipo_pagamento_id_tipo_pagamento int DEFAULT NULL,
  valor_pago decimal(10,2) DEFAULT NULL,
  data_pagamento timestamp DEFAULT NULL,
  DataHoraOperacao timestamp DEFAULT CURRENT_TIMESTAMP,
  ExecutedBy varchar(100) DEFAULT NULL
);

CREATE TABLE odontologista (
  id_odontologista SERIAL PRIMARY KEY,
  nome_odontologista varchar(100) DEFAULT NULL,
  especialidade varchar(100) DEFAULT NULL,
  cro varchar(20) DEFAULT NULL
);

CREATE TABLE paciente (
  id_paciente SERIAL PRIMARY KEY,
  nome_paciente varchar(100) DEFAULT NULL,
  cpf_paciente varchar(11) DEFAULT NULL,
  telefone varchar(15) DEFAULT NULL,
  genero char(1) DEFAULT NULL,
  data_nasc date DEFAULT NULL,
  email varchar(100) DEFAULT NULL,
  endereco_id_endereco int DEFAULT NULL
);

CREATE TABLE pagamento (
  id_pagamento SERIAL PRIMARY KEY,
  valor_pago decimal(10,2) DEFAULT NULL,
  data_pagamento timestamp DEFAULT NULL,
  tipo_pagamento_id_tipo_pagamento int NOT NULL,
  consulta_id_consulta int NOT NULL
);

CREATE TABLE procedimento (
  id_procedimento SERIAL PRIMARY KEY,
  nome_procedimento varchar(100) DEFAULT NULL,
  descricao_procedimento varchar(100) DEFAULT NULL
);

CREATE TABLE tipo_pagamento (
  id_tipo_pagamento SERIAL PRIMARY KEY,
  descricao_tipo_pagamento varchar(100) DEFAULT NULL
);

CREATE INDEX fk_agendamento_paciente1 ON agendamento (paciente_id_paciente);
CREATE INDEX fk_agendamento_odontologista1 ON agendamento (odontologista_id_odontologista);
CREATE INDEX fk_consulta_agendamento1 ON consulta (agendamento_id_agendamento);
CREATE INDEX fk_consulta_procedimento_consulta1 ON consulta_procedimento (consulta_id_consulta);
CREATE INDEX fk_consulta_procedimento_procedimento1 ON consulta_procedimento (procedimento_id_procedimento);
CREATE INDEX fk_paciente_endereco ON paciente (endereco_id_endereco);
CREATE INDEX fk_pagamento_consulta1 ON pagamento (consulta_id_consulta);
CREATE INDEX fk_pagamento_tipo_pagamento ON pagamento (tipo_pagamento_id_tipo_pagamento);

ALTER TABLE agendamento
  ADD CONSTRAINT fk_agendamento_odontologista1 FOREIGN KEY (odontologista_id_odontologista)
    REFERENCES odontologista (id_odontologista) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE agendamento
  ADD CONSTRAINT fk_agendamento_paciente1 FOREIGN KEY (paciente_id_paciente)
    REFERENCES paciente (id_paciente) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE consulta
  ADD CONSTRAINT fk_consulta_agendamento1 FOREIGN KEY (agendamento_id_agendamento)
    REFERENCES agendamento (id_agendamento) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE consulta_procedimento
  ADD CONSTRAINT fk_consulta_procedimento_consulta1 FOREIGN KEY (consulta_id_consulta)
    REFERENCES consulta (id_consulta) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE consulta_procedimento
  ADD CONSTRAINT fk_consulta_procedimento_procedimento1 FOREIGN KEY (procedimento_id_procedimento)
    REFERENCES procedimento (id_procedimento) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE paciente
  ADD CONSTRAINT fk_paciente_endereco FOREIGN KEY (endereco_id_endereco)
    REFERENCES endereco (id_endereco) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE pagamento
  ADD CONSTRAINT fk_pagamento_consulta1 FOREIGN KEY (consulta_id_consulta)
    REFERENCES consulta (id_consulta) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE pagamento
  ADD CONSTRAINT fk_pagamento_tipo_pagamento FOREIGN KEY (tipo_pagamento_id_tipo_pagamento)
    REFERENCES tipo_pagamento (id_tipo_pagamento) ON DELETE RESTRICT ON UPDATE CASCADE;
