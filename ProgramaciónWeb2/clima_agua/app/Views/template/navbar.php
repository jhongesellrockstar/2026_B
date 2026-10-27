<nav class="navegacion" aria-label="Navegación principal"><div class="contenedor">
<svg class="nav-simbolo garza-simbolo" viewBox="0 0 500 500" aria-hidden="true"><use href="<?= base_url('assets/img/garza.svg') ?>#silueta"></use></svg>
<?php foreach (['' => 'Inicio', 'fuentes' => 'Fuentes', 'variables' => 'Variables', 'categorias' => 'Categorías'] as $ruta => $etiqueta): ?>
    <a href="<?= site_url($ruta) ?>" <?= trim(uri_string(), '/') === $ruta ? 'aria-current="page"' : '' ?>><?= esc($etiqueta) ?></a>
<?php endforeach ?>
</div></nav>
