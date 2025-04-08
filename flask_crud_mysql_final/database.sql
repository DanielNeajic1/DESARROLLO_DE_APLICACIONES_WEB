-- Crear la base de datos si no existe
CREATE DATABASE desarrollo_web;

-- Usar la base de datos
USE desarrollo_web;

-- Crear la tabla productos si no existe
CREATE TABLE productos (
    id_producto INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    PRIMARY KEY (id_producto)
);