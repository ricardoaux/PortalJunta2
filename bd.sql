DROP TABLE noticia, pessoa, cidadao, administrador, conteudo_site CASCADE;

CREATE TABLE pessoa (
	id_pessoa SERIAL PRIMARY KEY, 
	nome varchar(50),
	permissao char(1) DEFAULT '0'
);

CREATE TABLE cidadao (
	id_pessoa SERIAL PRIMARY KEY, 
	nome varchar(50),
	permissao char(1) DEFAULT '0',
	num_bi integer,
	morada varchar(60),
	email varchar(50),
	telefone integer,
	nro_eleitor integer,
	newsletter char(1) DEFAULT '0'
)inherits(pessoa);

CREATE TABLE administrador (
	id_pessoa SERIAL PRIMARY KEY, 
	nome varchar(50),
	permissao char(1) DEFAULT '0'
)inherits(pessoa);

CREATE TABLE conteudo_site (
	id_conteudo SERIAL PRIMARY KEY,
	titulo varchar(100),
	descricao varchar (3000),
	data_insercao timestamp
);

CREATE TABLE noticia (
	id_conteudo SERIAL PRIMARY KEY,
	titulo varchar(100),
	descricao varchar (3000),
	data_insercao timestamp,
	imagem bytea
)inherits(conteudo_site);

INSERT INTO administrador (nome, permissao) VALUES ('admin', '1');
INSERT INTO noticia  (titulo, descricao, data_insercao) VALUES ('O Benfica ganhou', 'Um jogo muito complicado para a equipa da casa que fez com que o resultado fosse conseguido aos 92 minutos, por intermedio de Jonas Pistolas', to_timestamp('16-05-2011 15:36:38', 'dd-mm-yyyy hh24:mi:ss'));


COMMIT;

	
