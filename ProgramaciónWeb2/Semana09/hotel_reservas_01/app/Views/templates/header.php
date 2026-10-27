<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sistema de Reserva de Habitaciones</title>
    <link rel="stylesheet" href="<?= base_url('css/estilos.css') ?>">
</head>
<body>
<main class="contenedor">
    <p class="curso">Programación Web II · Gestión de habitaciones</p>
    <?php if ($mensaje = session()->getFlashdata('mensaje')): ?>
        <p class="mensaje" role="status"><?= esc($mensaje) ?></p>
    <?php endif ?>
    <?php if ($errores = session()->getFlashdata('errores')): ?>
        <div class="errores" role="alert"><ul>
            <?php foreach ($errores as $error): ?><li><?= esc($error) ?></li><?php endforeach ?>
        </ul></div>
    <?php endif ?>
