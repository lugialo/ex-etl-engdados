CREATE TABLE [agendamento] (
  [id_agendamento] int PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [data_agendamento] datetime DEFAULT (null),
  [status_agendamento] varchar(100) DEFAULT (null),
  [paciente_id_paciente] int NOT NULL,
  [odontologista_id_odontologista] int NOT NULL
)
GO

CREATE TABLE [consulta] (
  [id_consulta] int PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [data_hora] datetime DEFAULT (null),
  [diagnostico] longtext,
  [tratamento] longtext,
  [agendamento_id_agendamento] int NOT NULL
)
GO

CREATE TABLE [consulta_procedimento] (
  [id_consulta_procedimento] int NOT NULL IDENTITY(1, 1),
  [consulta_id_consulta] int NOT NULL,
  [procedimento_id_procedimento] int NOT NULL,
  PRIMARY KEY ([id_consulta_procedimento], [consulta_id_consulta], [procedimento_id_procedimento])
)
GO

CREATE TABLE [endereco] (
  [id_endereco] int PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [logradouro] varchar(255) NOT NULL,
  [numero] varchar(20) DEFAULT (null),
  [complemento] varchar(100) DEFAULT (null),
  [bairro] varchar(100) NOT NULL,
  [cidade] varchar(100) NOT NULL,
  [estado] char(2) NOT NULL,
  [cep] varchar(9) NOT NULL,
  [pais] varchar(200) NOT NULL
)
GO

CREATE TABLE [log_pagamento] (
  [id_log] int PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [tipo_acao] varchar(10) NOT NULL,
  [id_pagamento] int NOT NULL,
  [tipo_pagamento_id_tipo_pagamento] int DEFAULT (null),
  [valor_pago] decimal(10,2) DEFAULT (null),
  [data_pagamento] datetime DEFAULT (null),
  [DataHoraOperacao] timestamp DEFAULT (CURRENT_TIMESTAMP),
  [ExecutedBy] varchar(100) DEFAULT (null)
)
GO

CREATE TABLE [odontologista] (
  [id_odontologista] int PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [nome_odontologista] varchar(100) DEFAULT (null),
  [especialidade] varchar(100) DEFAULT (null),
  [cro] varchar(20) DEFAULT (null)
)
GO

CREATE TABLE [paciente] (
  [id_paciente] int PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [nome_paciente] varchar(100) DEFAULT (null),
  [cpf_paciente] varchar(11) DEFAULT (null),
  [telefone] varchar(15) DEFAULT (null),
  [genero] char(1) DEFAULT (null),
  [data_nasc] date DEFAULT (null),
  [email] varchar(100) DEFAULT (null),
  [endereco_id_endereco] int DEFAULT (null)
)
GO

CREATE TABLE [pagamento] (
  [id_pagamento] int PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [valor_pago] decimal(10,2) DEFAULT (null),
  [data_pagamento] datetime DEFAULT (null),
  [tipo_pagamento_id_tipo_pagamento] int NOT NULL,
  [consulta_id_consulta] int NOT NULL
)
GO

CREATE TABLE [procedimento] (
  [id_procedimento] int PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [nome_procedimento] varchar(100) DEFAULT (null),
  [descricao_procedimento] varchar(100) DEFAULT (null)
)
GO

CREATE TABLE [tipo_pagamento] (
  [id_tipo_pagamento] int PRIMARY KEY NOT NULL IDENTITY(1, 1),
  [descricao_tipo_pagamento] varchar(100) DEFAULT (null)
)
GO

CREATE INDEX [fk_agendamento_paciente1] ON [agendamento] ("paciente_id_paciente")
GO

CREATE INDEX [fk_agendamento_odontologista1] ON [agendamento] ("odontologista_id_odontologista")
GO

CREATE INDEX [fk_consulta_agendamento1] ON [consulta] ("agendamento_id_agendamento")
GO

CREATE INDEX [fk_consulta_procedimento_consulta1] ON [consulta_procedimento] ("consulta_id_consulta")
GO

CREATE INDEX [fk_consulta_procedimento_procedimento1] ON [consulta_procedimento] ("procedimento_id_procedimento")
GO

CREATE INDEX [fk_paciente_endereco] ON [paciente] ("endereco_id_endereco")
GO

CREATE INDEX [fk_pagamento_consulta1] ON [pagamento] ("consulta_id_consulta")
GO

CREATE INDEX [fk_pagamento_tipo_pagamento] ON [pagamento] ("tipo_pagamento_id_tipo_pagamento")
GO

ALTER TABLE [agendamento] ADD CONSTRAINT [fk_agendamento_odontologista1] FOREIGN KEY ([odontologista_id_odontologista]) REFERENCES [odontologista] ([id_odontologista]) ON DELETE CASCADE ON UPDATE CASCADE
GO

ALTER TABLE [agendamento] ADD CONSTRAINT [fk_agendamento_paciente1] FOREIGN KEY ([paciente_id_paciente]) REFERENCES [paciente] ([id_paciente]) ON DELETE CASCADE ON UPDATE CASCADE
GO

ALTER TABLE [consulta] ADD CONSTRAINT [fk_consulta_agendamento1] FOREIGN KEY ([agendamento_id_agendamento]) REFERENCES [agendamento] ([id_agendamento]) ON DELETE CASCADE ON UPDATE CASCADE
GO

ALTER TABLE [consulta_procedimento] ADD CONSTRAINT [fk_consulta_procedimento_consulta1] FOREIGN KEY ([consulta_id_consulta]) REFERENCES [consulta] ([id_consulta]) ON DELETE CASCADE ON UPDATE CASCADE
GO

ALTER TABLE [consulta_procedimento] ADD CONSTRAINT [fk_consulta_procedimento_procedimento1] FOREIGN KEY ([procedimento_id_procedimento]) REFERENCES [procedimento] ([id_procedimento]) ON DELETE CASCADE ON UPDATE CASCADE
GO

ALTER TABLE [paciente] ADD CONSTRAINT [fk_paciente_endereco] FOREIGN KEY ([endereco_id_endereco]) REFERENCES [endereco] ([id_endereco]) ON DELETE SET NULL ON UPDATE CASCADE
GO

ALTER TABLE [pagamento] ADD CONSTRAINT [fk_pagamento_consulta1] FOREIGN KEY ([consulta_id_consulta]) REFERENCES [consulta] ([id_consulta]) ON DELETE RESTRICT ON UPDATE CASCADE
GO

ALTER TABLE [pagamento] ADD CONSTRAINT [fk_pagamento_tipo_pagamento] FOREIGN KEY ([tipo_pagamento_id_tipo_pagamento]) REFERENCES [tipo_pagamento] ([id_tipo_pagamento]) ON DELETE RESTRICT ON UPDATE CASCADE
GO
