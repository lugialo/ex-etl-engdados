CREATE TABLE IF NOT EXISTS fato_consulta_pagamento (
  id_fato SERIAL PRIMARY KEY,
  id_consulta int NOT NULL,
  id_paciente int NOT NULL,
  id_odontologista int NOT NULL,
  id_procedimento int NOT NULL,
  id_tipo_pagamento int NOT NULL,
  id_tempo int NOT NULL,
  valor_pago numeric(10,2),
  quantidade_procedimentos int
);

CREATE TABLE IF NOT EXISTS dim_paciente (
  id_paciente int PRIMARY KEY,
  nome_paciente varchar(100),
  cpf_paciente varchar(11),
  genero char(1),
  data_nasc date,
  cidade varchar(100),
  estado char(2),
  pais varchar(200)
);

CREATE TABLE IF NOT EXISTS dim_odontologista (
  id_odontologista int PRIMARY KEY,
  nome_odontologista varchar(100),
  especialidade varchar(100),
  cro varchar(20)
);

CREATE TABLE IF NOT EXISTS dim_procedimento (
  id_procedimento int PRIMARY KEY,
  nome_procedimento varchar(100),
  descricao_procedimento varchar(100)
);

CREATE TABLE IF NOT EXISTS dim_consulta (
  id_consulta int PRIMARY KEY,
  data_hora timestamp DEFAULT NULL,
  diagnostico text,
  tratamento text,
  id_agendamento int
);

CREATE TABLE IF NOT EXISTS dim_tipo_pagamento (
  id_tipo_pagamento int PRIMARY KEY,
  descricao_tipo_pagamento varchar(100)
);

CREATE TABLE IF NOT EXISTS dim_tempo (
  id_tempo int PRIMARY KEY,
  data date,
  ano int,
  mes int,
  dia int,
  dia_semana varchar(20)
);

ALTER TABLE fato_consulta_pagamento ADD CONSTRAINT fk_fato_paciente FOREIGN KEY (id_paciente) REFERENCES dim_paciente (id_paciente) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE fato_consulta_pagamento ADD CONSTRAINT fk_fato_odontologista FOREIGN KEY (id_odontologista) REFERENCES dim_odontologista (id_odontologista) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE fato_consulta_pagamento ADD CONSTRAINT fk_fato_consulta FOREIGN KEY (id_consulta) REFERENCES dim_consulta (id_consulta) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE fato_consulta_pagamento ADD CONSTRAINT fk_fato_procedimento FOREIGN KEY (id_procedimento) REFERENCES dim_procedimento (id_procedimento) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE fato_consulta_pagamento ADD CONSTRAINT fk_fato_pagamento FOREIGN KEY (id_tipo_pagamento) REFERENCES dim_tipo_pagamento (id_tipo_pagamento) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE fato_consulta_pagamento ADD CONSTRAINT fk_fato_tempo FOREIGN KEY (id_tempo) REFERENCES dim_tempo (id_tempo) ON DELETE CASCADE ON UPDATE CASCADE;
