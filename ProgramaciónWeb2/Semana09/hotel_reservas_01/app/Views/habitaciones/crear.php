<?= view('templates/header') ?>

<h1>Nueva habitación</h1>
<form class="formulario" method="post" action="<?= site_url('habitaciones/guardar') ?>">
    <?= csrf_field() ?>
    <label for="codigo">Código</label>
    <input id="codigo" name="codigo" maxlength="20" required value="<?= esc(old('codigo'), 'attr') ?>" placeholder="HAB-010">

    <label for="tipo">Tipo</label>
    <select id="tipo" name="tipo" required>
        <option value="">Seleccione</option>
        <option value="sencilla" <?= old('tipo') === 'sencilla' ? 'selected' : '' ?>>Sencilla</option>
        <option value="doble" <?= old('tipo') === 'doble' ? 'selected' : '' ?>>Doble</option>
        <option value="triple" <?= old('tipo') === 'triple' ? 'selected' : '' ?>>Triple</option>
    </select>

    <label for="capacidad">Capacidad máxima de huéspedes</label>
    <input id="capacidad" name="capacidad" type="number" readonly aria-describedby="tarifa">
    <label for="precio_noche">Precio por noche (S/)</label>
    <input id="precio_noche" name="precio_noche" type="number" step="0.01" readonly>
    <p id="tarifa" class="ayuda">Capacidad y precio se asignan según el tipo, también en el servidor.</p>

    <label for="estado">Estado</label>
    <select id="estado" name="estado" required>
        <option value="disponible" <?= old('estado', 'disponible') === 'disponible' ? 'selected' : '' ?>>Disponible</option>
        <option value="mantenimiento" <?= old('estado') === 'mantenimiento' ? 'selected' : '' ?>>Mantenimiento</option>
        <option value="ocupada" <?= old('estado') === 'ocupada' ? 'selected' : '' ?>>Ocupada</option>
    </select>

    <label for="fecha">Fecha</label>
    <input id="fecha" name="fecha" type="date" required value="<?= esc(old('fecha', date('Y-m-d')), 'attr') ?>">
    <div class="botones">
        <button class="principal" type="submit">Guardar</button>
        <a class="boton" href="<?= site_url('habitaciones') ?>">Cancelar</a>
    </div>
</form>

<?= view('templates/footer') ?>
