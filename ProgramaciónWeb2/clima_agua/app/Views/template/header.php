<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= esc($titulo) ?> | CLIMA Y AGUA</title>
    <link rel="icon" type="image/svg+xml" href="<?= base_url('favicon.svg') ?>">
    <link rel="stylesheet" href="<?= base_url('css/estilos.css') ?>?v=2">
    <script src="<?= base_url('js/fuentes.js') ?>" defer></script>
</head>
<body>
<header class="cabecera"><div class="contenedor marca">
    <svg class="logo garza-simbolo" viewBox="0 0 500 500" aria-hidden="true"><use href="<?= base_url('assets/img/garza.svg') ?>#silueta"></use></svg>
    <div><a href="<?= site_url() ?>" class="nombre">CLIMA Y AGUA</a><p>Datos para tu investigación</p></div>
    <span class="garza">GARZA <small>Datos para investigar</small></span>
</div></header>
<?= view('template/navbar') ?>
<main class="contenedor">
<?php if ($mensaje = session()->getFlashdata('mensaje')): ?>
    <p class="aviso" role="status"><?= esc($mensaje) ?></p>
<?php endif ?>
