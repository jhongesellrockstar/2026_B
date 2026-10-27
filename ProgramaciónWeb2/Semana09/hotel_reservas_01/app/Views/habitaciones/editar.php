<?= view('templates/header') ?>

<h1>Editar habitación</h1>
<form class="formulario" method="post" action="<?= site_url('habitaciones/actualizar/' . $habitacion['id']) ?>">
    <?= csrf_field() ?>
    <label for="codigo">Código</label>
    <input id="codigo" name="codigo" maxlength="20" required value="<?= esc(old('codigo', $habitacion['codigo']), 'attr') ?>">

    <label for="tipo">Tipo</label>
    <select id="tipo" name="tipo" required>
        <option value="sencilla" <?= old('tipo', $habitacion['tipo']) === 'sencilla' ? 'selected' : '' ?>>Sencilla</option>
        <option value="doble" <?= old('tipo', $habitacion['tipo']) === 'doble' ? 'selected' : '' ?>>Doble</option>
        <option value="triple" <?= old('tipo', $habitacion['tipo']) === 'triple' ? 'selected' : '' ?>>Triple</option>
    </select>

    <label for="capacidad">Capacidad máxima de huéspedes</label>
    <input id="capacidad" name="capacidad" type="number" readonly value="<?= esc($habitacion['capacidad'], 'attr') ?>" aria-describedby="tarifa">
    <label for="precio_noche">Precio por noche (S/)</label>
    <input id="precio_noche" name="precio_noche" type="number" step="0.01" readonly value="<?= esc($habitacion['precio_noche'], 'attr') ?>">
    <p id="tarifa" class="ayuda">Al cambiar de tipo se recalculan la capacidad y el precio.</p>

    <label for="estado">Estado</label>
    <select id="estado" name="estado" required>
        <option value="disponible" <?= old('estado', $habitacion['estado']) === 'disponible' ? 'selected' : '' ?>>Disponible</option>
        <option value="mantenimiento" <?= old('estado', $habitacion['estado']) === 'mantenimiento' ? 'selected' : '' ?>>Mantenimiento</option>
        <option value="ocupada" <?= old('estado', $habitacion['estado']) === 'ocupada' ? 'selected' : '' ?>>Ocupada</option>
    </select>

    <label for="fecha">Fecha</label>
    <input id="fecha" name="fecha" type="date" required value="<?= esc(old('fecha', $habitacion['fecha']), 'attr') ?>">
    <div class="botones">
        <button class="principal" type="submit">Actualizar</button>
        <a class="boton" href="<?= site_url('habitaciones') ?>">Cancelar</a>
    </div>
</form>

<?= view('templates/footer') ?>
