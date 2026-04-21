create database company;
use company;
drop database company;

create table departamentos(
id_area int auto_increment primary key,
area varchar(50) not null
);

INSERT INTO `departamentos` (`id_area`, `area`) VALUES
(1, 'Computación'),
(2, 'RRHH');

create table empleados(
id int auto_increment primary key,
documento varchar(50) unique not null,
nombre varchar(50) not null,
apellido varchar(50) not null,
cargo varchar(50) not null,
salariobase decimal(10,2) not null,
horasextras int,
bonificacion decimal(10,2),
salud decimal(10,2),
pension decimal(10,2),
salarioneto decimal(10,2),
id_dep int,
foreign key (id_dep)references departamentos(id_area)
);

INSERT INTO `empleados` (`id`, `documento`, `nombre`, `apellido`, `cargo`, `salariobase`, `horasextras`, `bonificacion`, `salud`, `pension`, `salarioneto`) VALUES
(1, '45623', 'Nigga', 'Sanchez', 'Contador', 45.00, 300000, 3235000.00, 129400.00, 129400.00, 2976200.00),
(2, '1462', 'Gero', 'Rosas', 'empleado', 30.00, 20000, 2910000.00, 116400.00, 116400.00, 2677200.00);

create table usuarios(
id_usu int auto_increment primary  key NOT NULL,
usuario varchar(50) NOT NULL,
password varchar(255) NOT NULL,
rol varchar(255) NOT NULL,
documento varchar(20) NOT NULL);

INSERT INTO `usuarios` (`id_usu`, `usuario`, `password`, `rol`, `documento`) VALUES
(2, 'ADMIN', '1010', 'administrador', NULL),
(3, 'AKX', '1111', 'empleado', '516568');


