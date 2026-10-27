<?= view('templates/header') ?>

<h1>Sistema de Reserva de Habitaciones</h1>
<p>Registra habitaciones y actualiza su tipo, estado y fecha.</p>
<a class="boton principal" href="<?= site_url('habitaciones/crear') ?>">Nueva habitación</a>

<div class="tabla">
<table>
    <thead><tr>
        <th scope="col">ID</th>
        <th scope="col">Código</th>
        <th scope="col">Tipo</th>
        <th scope="col">Capacidad</th>
        <th scope="col">Precio por noche</th>
        <th scope="col">Estado</th>
        <th scope="col">Fecha</th>
        <th scope="col">Acciones</th>
    </tr></thead>
    <tbody>
    <?php foreach ($habitaciones as $habitacion): ?>
        <tr>
            <td><?= esc($habitacion['id']) ?></td>
            <td><?= esc($habitacion['codigo']) ?></td>
            <td><?= esc($habitacion['tipo']) ?></td>
            <td><?= esc($habitacion['capacidad']) ?></td>
            <td>S/ <?= number_format((float) $habitacion['precio_noche'], 2) ?></td>
            <td><?= esc($habitacion['estado']) ?></td>
            <td><?= esc($habitacion['fecha']) ?></td>
            <td class="acciones">
                <a href="<?= site_url('habitaciones/editar/' . $habitacion['id']) ?>">Editar</a>
                <form method="post" action="<?= site_url('habitaciones/eliminar/' . $habitacion['id']) ?>" onsubmit="return confirm('¿Eliminar esta habitación?')">
                    <?= csrf_field() ?>
                    <button class="eliminar" type="submit">Eliminar</button>
                </form>
            </td>
        </tr>
    <?php endforeach ?>
    <?php if (!$habitaciones): ?><tr><td colspan="8">No hay habitaciones registradas.</td></tr><?php endif ?>
    </tbody>
</table>
</div>

<?= view('templates/footer') ?>
