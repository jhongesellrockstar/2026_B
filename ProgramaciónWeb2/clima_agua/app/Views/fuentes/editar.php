<?= view('template/header') ?>
<a class="volver" href="<?= site_url('fuentes') ?>">← Volver al catálogo</a>
<section class="panel"><h1>Editar fuente</h1><p>Actualiza las características de <?= esc($fuente['nombre']) ?>.</p>
<?= view('fuentes/formulario', ['accion' => site_url('fuentes/actualizar/' . $fuente['id'])]) ?></section>
<?= view('template/footer') ?>
