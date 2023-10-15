CREATE TABLE usuarios(
    dni CHAR(9) PRIMARY KEY NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefono CHAR(9) NOT NULL,
    salt BLOB NOT NULL,
    encryped_pass BLOB NOT NULL
);