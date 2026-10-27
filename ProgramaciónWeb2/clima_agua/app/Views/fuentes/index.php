<?= view('template/header') ?>
<section class="presentacion">
    <div class="presentacion-texto">
    <p class="sobrelinea">DATOS PARA TU INVESTIGACIÓN</p>
    <h1>CLIMA Y AGUA</h1>
    <h2>Catálogo de fuentes de datos hidroclimáticos<br> para investigación universitaria.</h2>
    <p>Encuentra fuentes nacionales e internacionales de información meteorológica, hidrológica y oceanográfica.</p>
    </div>
    <svg class="hero-garza garza-simbolo" viewBox="0 0 500 500" aria-hidden="true"><use href="<?= base_url('assets/img/garza.svg') ?>#silueta"></use></svg>
</section>
<section class="panel" aria-labelledby="titulo-fuentes">
    <div class="fila titulo-seccion"><div><p class="sobrelinea">EXPLORA EL CATÁLOGO</p><h2 id="titulo-fuentes">Fuentes de datos</h2></div>
        <a class="boton" href="<?= site_url('fuentes/crear') ?>">+ Registrar fuente</a></div>
    <form id="buscador" method="get" action="<?= site_url('fuentes') ?>" data-ajax="<?= site_url('fuentes/buscar') ?>">
        <div class="filtros">
            <label class="busqueda">Buscar fuente<input type="search" name="q" id="q" value="<?= esc($q) ?>" placeholder="Buscar fuente..." maxlength="200"><small>Nombre, institución, cobertura o variable</small></label>
            <label>Categoría<select name="categoria"><option value="">Todas las categorías</option>
            <?php foreach ($categorias as $item): ?><option value="<?= $item['id'] ?>" <?= (string) $item['id'] === $categoriaSeleccionada ? 'selected' : '' ?>><?= esc($item['nombre']) ?></option><?php endforeach ?>
            </select></label>
            <label>Ámbito<select name="ambito"><option value="">Todos los ámbitos</option>
            <?php foreach ($ambitos as $item): ?><option value="<?= $item['id'] ?>" <?= (string) $item['id'] === $ambitoSeleccionado ? 'selected' : '' ?>><?= esc($item['nombre']) ?></option><?php endforeach ?>
            </select></label>
            <button type="submit">Buscar</button><a class="limpiar" href="<?= site_url('fuentes') ?>">Limpiar</a>
        </div>
    </form>
    <p id="estado-busqueda" class="ayuda" role="status">Búsqueda dinámica con AJAX · la tabla se actualiza mientras escribes.</p>
    <div id="resultados"><?= view('fuentes/tabla') ?></div>
</section>
<?= view('template/footer') ?>
