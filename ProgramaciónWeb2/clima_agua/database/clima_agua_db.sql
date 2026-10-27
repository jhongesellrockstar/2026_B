-- Importar una sola vez en phpMyAdmin. No elimina bases ni tablas existentes.
CREATE DATABASE IF NOT EXISTS clima_agua_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE clima_agua_db;
SET NAMES utf8mb4;

CREATE TABLE categorias (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(100) NOT NULL,
 descripcion TEXT
) ENGINE=InnoDB;
CREATE TABLE ambitos (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(100) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE variables (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(100) NOT NULL,
 unidad VARCHAR(80),
 descripcion TEXT
) ENGINE=InnoDB;
CREATE TABLE fuentes (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(150) NOT NULL,
 institucion VARCHAR(200) NOT NULL,
 descripcion TEXT,
 categoria_id INT UNSIGNED NOT NULL,
 ambito_id INT UNSIGNED NOT NULL,
 variable_id INT UNSIGNED NOT NULL,
 cobertura VARCHAR(200),
 resolucion_espacial VARCHAR(200),
 resolucion_temporal VARCHAR(200),
 periodo_disponible VARCHAR(200),
 formato VARCHAR(200),
 tipo_acceso VARCHAR(50) NOT NULL DEFAULT 'Por verificar',
 url VARCHAR(500),
 estado ENUM('Activo','Inactivo') NOT NULL DEFAULT 'Activo',
 created_at DATETIME NOT NULL,
 updated_at DATETIME NOT NULL,
 CONSTRAINT fk_fuente_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id),
 CONSTRAINT fk_fuente_ambito FOREIGN KEY (ambito_id) REFERENCES ambitos(id),
 CONSTRAINT fk_fuente_variable FOREIGN KEY (variable_id) REFERENCES variables(id)
) ENGINE=InnoDB;

INSERT INTO categorias (nombre, descripcion) VALUES
('Meteorología','Fuentes relacionadas con las condiciones de la atmósfera.'),
('Hidrología','Fuentes sobre el agua continental y su comportamiento.'),
('Oceanografía','Fuentes sobre el océano y el ambiente marino.'),
('Climatología','Fuentes para estudiar el clima y su variabilidad.');
INSERT INTO ambitos (nombre) VALUES
('Cuenca hidrográfica'),('Río'),('Lago'),('Océano'),('Atmósfera');
INSERT INTO variables (nombre, unidad, descripcion) VALUES
('Precipitación','mm','Unidad orientativa; consultar la definición y acumulación temporal de cada producto.'),
('Caudal','m³/s','Volumen de agua que atraviesa una sección por unidad de tiempo.'),
('Nivel del agua','m','El nivel requiere un punto de referencia definido por la fuente.'),
('Temperatura superficial del mar','°C','Consultar la definición y unidad de cada producto.'),
('Oleaje','Según producto','Incluye características como altura, periodo y dirección.'),
('Corrientes','Según producto','Consultar componentes, profundidad y unidades del producto.'),
('Varias variables','Según producto','Un portal puede contener varias variables y productos.');

-- Catálogo DEMOSTRATIVO: cobertura general y asociación temática orientativa.
-- No se atribuyen resoluciones, periodos, formatos ni permisos sin verificar.
INSERT INTO fuentes
(nombre,institucion,descripcion,categoria_id,ambito_id,variable_id,cobertura,url,created_at,updated_at) VALUES
('PISCO','SENAMHI','Ejemplo de fuente para investigar precipitación. Verificar la versión y documentación del producto.',1,5,1,'Perú','https://www.senamhi.gob.pe/',NOW(),NOW()),
('CHIRPS','Climate Hazards Center (CHC), UCSB','Fuente de estimaciones de precipitación. Consultar la cobertura exacta de la versión seleccionada.',1,5,1,'Internacional; consultar límites del producto','https://www.chc.ucsb.edu/data/chirps3',NOW(),NOW()),
('GPM','NASA','Misión relacionada con la medición de precipitación. Seleccionar un producto en su directorio.',1,5,1,'Internacional; según producto','https://gpm.nasa.gov/data/directory',NOW(),NOW()),
('ERA5','ECMWF / Copernicus','Reanálisis con múltiples variables. Consultar la documentación del conjunto elegido.',4,5,7,'Global','https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5',NOW(),NOW()),
('RAIN4PE','Equipo de investigación RAIN4PE','Registro demostrativo de una fuente de precipitación. Revisar autores, versión y alcance en la publicación original.',1,5,1,'Perú y Ecuador; verificar producto','',NOW(),NOW()),
('SENAMHI - estaciones hidrológicas','SENAMHI','Portal institucional de referencia para explorar observaciones hidrológicas.',2,2,2,'Perú; según estación','https://www.senamhi.gob.pe/',NOW(),NOW()),
('ANA','Autoridad Nacional del Agua','Portal institucional de referencia para recursos hídricos. La disponibilidad depende del conjunto consultado.',2,1,7,'Perú','https://www.ana.gob.pe/',NOW(),NOW()),
('DIHIDRONAV','Dirección de Hidrografía y Navegación','Portal institucional de referencia para información hidrográfica y oceanográfica.',3,4,7,'Perú; según producto','https://www.dhn.mil.pe/',NOW(),NOW()),
('Copernicus Marine','Servicio Marino de Copernicus','Catálogo de productos del medio marino; consultar variables y condiciones de cada producto.',3,4,7,'Internacional; según producto','https://marine.copernicus.eu/',NOW(),NOW()),
('NOAA','NOAA','Portal institucional con información atmosférica y oceánica. Seleccionar un conjunto específico.',3,4,7,'Internacional; según producto','https://www.noaa.gov/',NOW(),NOW()),
('NASA Earthdata','NASA','Portal de referencia para conjuntos de datos de ciencias de la Tierra.',1,5,7,'Internacional; según producto','https://www.earthdata.nasa.gov/',NOW(),NOW()),
('Climate Data Store','Copernicus Climate Change Service','Catálogo de referencia para datos del clima. Verificar las condiciones del producto.',4,5,7,'Internacional; según producto','https://cds.climate.copernicus.eu/',NOW(),NOW()),
('IMARPE','Instituto del Mar del Perú','Portal institucional de referencia para investigación del ambiente marino.',3,4,7,'Perú; según producto','https://www.imarpe.gob.pe/',NOW(),NOW()),
('USGS Water Data','USGS','Portal de referencia para observaciones de agua; consultar estaciones y variables disponibles.',2,2,7,'Estados Unidos; según estación','https://waterdata.usgs.gov/',NOW(),NOW()),
('IDEAM','IDEAM','Portal institucional de referencia para información hidrológica, meteorológica y ambiental.',2,1,7,'Colombia; según producto','https://www.ideam.gov.co/',NOW(),NOW());

UPDATE fuentes SET resolucion_espacial='Por verificar', resolucion_temporal='Por verificar',
 periodo_disponible='Por verificar', formato='Por verificar';
