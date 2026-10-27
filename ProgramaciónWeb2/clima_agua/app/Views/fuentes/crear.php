<?= view('template/header') ?>
<a class="volver" href="<?= site_url('fuentes') ?>">← Volver al catálogo</a>
<section class="panel"><h1>Registrar fuente</h1><p>Agrega una fuente y sus características para orientar la investigación.</p>
<?php $accion = site_url('fuentes/guardar'); ?>
<?= view('fuentes/formulario', ['accion' => $accion]) ?></section>
<?= view('template/footer') ?>
