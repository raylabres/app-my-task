create database lista_tarefas;
use lista_tarefas;

create table usuarios (
	id int auto_increment,
    nome varchar(100) not null,
    usuario varchar(50) unique not null,
    senha varchar(50) not null,
    primary key(id)
);

create table tarefas (
	id int auto_increment,
    nome varchar(50) not null,
    descricao varchar(255) not null,
    data_inicio date not null,
    data_fim date not null,
    status_tarefa enum('Pendente', 'Andamento', 'Finalizado') default("Pendente"),
    primary key(id),
    CHECK (nome <> '' AND descricao <> '' AND data_inicio <> '' AND data_fim <> '')
);

create table usuario_recebe_tarefa (
	id_usuario int,
    id_tarefa int,
    foreign key(id_usuario) references usuarios(id),
    foreign key(id_tarefa) references tarefas(id)
);

show tables;
desc usuarios;
desc tarefas;
desc usuario_recebe_tarefa;