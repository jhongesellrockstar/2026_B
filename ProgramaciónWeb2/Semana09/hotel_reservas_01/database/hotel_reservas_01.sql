-- Estructura y datos de demostración para importar en phpMyAdmin.
CREATE DATABASE IF NOT EXISTS hotel_reservas_01
CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE hotel_reservas_01;

CREATE TABLE IF NOT EXISTS habitaciones (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    tipo ENUM('sencilla', 'doble', 'triple') NOT NULL,
    capacidad INT UNSIGNED NOT NULL,
    precio_noche DECIMAL(10,2) UNSIGNED NOT NULL,
    estado ENUM('disponible', 'mantenimiento', 'ocupada') NOT NULL,
    fecha DATE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Al repetir la importación no duplicamos los códigos de ejemplo.
INSERT IGNORE INTO habitaciones (codigo, tipo, capacidad, precio_noche, estado, fecha) VALUES
('H101', 'sencilla', 1, 100.00, 'disponible', '2026-10-27'),
('H102', 'doble', 2, 200.00, 'ocupada', '2026-10-27'),
('H103', 'triple', 3, 300.00, 'mantenimiento', '2026-10-27');
