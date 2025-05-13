USE AgenteResiduosDB;

CREATE TABLE residuos (
    id_residuo INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(100),
    tipo VARCHAR(50),
    contenedor VARCHAR(50),
    observaciones TEXT
);
CREATE TABLE alimentos (
    id_alimento INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(100),
    propiedad VARCHAR(50),  
    categoria VARCHAR(50),  
    observaciones TEXT
);


CREATE TABLE peliculas (
    id_pelicula INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(100),
    genero VARCHAR(50),
    sinopsis TEXT
);

USE AgenteResiduosDB;
GO


CREATE TABLE reglas (
    id_regla INT PRIMARY KEY IDENTITY(1,1),
    palabra_clave VARCHAR(100),
    tipo VARCHAR(50),
    contenedor VARCHAR(50),
    observaciones TEXT
);

CREATE TABLE reglas_alimentos (
    id_regla INT PRIMARY KEY IDENTITY(1,1),
    palabra_clave VARCHAR(100),
    propiedad VARCHAR(50),
    categoria VARCHAR(50),
    observaciones TEXT
);

select * from peliculas;

CREATE TABLE reglas_peliculas (
    id_regla INT PRIMARY KEY IDENTITY(1,1),
    palabra_clave VARCHAR(100),
    genero VARCHAR(50),
    sinopsis TEXT
);






INSERT INTO residuos (nombre, tipo, contenedor, observaciones) VALUES
('botella de plástico', 'reciclable', 'blanco', 'Debe estar limpia antes de desecharse'),
('cáscara de plátano', 'orgánico', 'verde', 'Puede servir como abono'),
('pilas usadas', 'no reciclable', 'negro', 'Es un riesgo biológico'),
('papel sucio', 'no reciclable', 'negro', 'El papel sucio no se recicla correctamente'),
('botella de vidrio', 'vidrio', 'rojo', 'Debe enjuagarse antes de desecharse'),
('frasco de vidrio', 'vidrio', 'rojo', 'Puede reciclarse si no está quebrado'),
('bolsa plástica', 'reciclable', 'blanco', 'Evitar que esté sucia'),
('restos de fruta', 'orgánico', 'verde', 'Puede servir como abono');

select * from residuos;

INSERT INTO alimentos (nombre, propiedad, categoria, observaciones) VALUES
('pizza', 'grasoso', 'comida rápida', 'puede ser rico pero no saludable'),
('zanahoria', 'saludable', 'vegetal', 'bueno para la visa'),
('pera', 'saludable', 'fruta', 'Es una fruta rica y saludable'),
('hamburguesa', 'grasoso', 'comida rapida', 'Es una fruta rica y saludable');

select * from alimentos;


INSERT INTO peliculas (nombre, genero, sinopsis) VALUES
('chucky', 'terror', 'muñeco poseído que mata personas'),
('Spiderman', 'acción', 'Hombre que tiene poderes de una araña'),
('Minecraft', 'videojuegos', 'Un mundo diferente al que se conoce lleno de cuadritos');


select * from peliculas;

