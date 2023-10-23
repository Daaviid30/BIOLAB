CREATE TABLE usuarios(
    dni CHAR(9) PRIMARY KEY NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefono CHAR(9) NOT NULL,
    salt BLOB NOT NULL,
    encryped_pass BLOB NOT NULL
);


CREATE TABLE papers(
    dni CHAR(9) NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    cuerpo BLOB NOT NULL,
    salt BLOB NOT NULL,
    nonce BLOB NOT NULL,
    PRIMARY KEY (dni,titulo),
    FOREIGN KEY (dni) REFERENCES usuarios(dni)
);