<?= view('template/header') ?>
<section class="panel catalogos"><p class="sobrelinea">GUÍA DEL CATÁLOGO</p><h1><?= esc($titulo) ?></h1>
<p>Referencias utilizadas para clasificar las fuentes de datos.</p>
<?php foreach ($filas as $fila): ?><article><h2><?= esc($fila['nombre']) ?></h2><p><?= esc($fila['descripcion']) ?></p><?php if (isset($fila['unidad'])): ?><small>Unidad orientativa: <?= esc($fila['unidad']) ?></small><?php endif ?></article><?php endforeach ?>
</section><?= view('template/footer') ?>
