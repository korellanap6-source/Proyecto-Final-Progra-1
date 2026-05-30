
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS calibracion_tanques (
    id SERIAL PRIMARY KEY,
    combustible VARCHAR(20) NOT NULL,
    pulgadas NUMERIC NOT NULL,
    galones NUMERIC NOT NULL
);


CREATE TABLE IF NOT EXISTS registros_medidas (
    id SERIAL PRIMARY KEY,
    fecha DATE UNIQUE NOT NULL,
    
    diesel_pulg NUMERIC NOT NULL,
    diesel_gls NUMERIC NOT NULL,
    diesel_venta NUMERIC NOT NULL,
    
    regular_pulg NUMERIC NOT NULL,
    regular_gls NUMERIC NOT NULL,
    regular_venta NUMERIC NOT NULL,
    
    super_pulg NUMERIC NOT NULL,
    super_gls NUMERIC NOT NULL,
    super_venta NUMERIC NOT NULL
);

INSERT INTO usuarios (username, password, rol) 
VALUES 
('Kevin', '1234', 'admin'),
('Maria', '5678', 'empleado'), 
('Luis', '5678', 'empleado'),
('Brayan', '1234', 'admin'),
('Irvyn', '1234', 'admin'),
('Erick', '1234', 'admin');
