<h1>Listado de Usuarios</h1>

<!-- Enlace para el siguiente paso del CRUD -->
<a href="<?= base_url('public/usuario/crear') ?>">Crear Nuevo Usuario</a>
<br><br>

<table border="1" cellpadding="10" cellspacing="0">
    <thead>
        <tr>
            <th>ID</th>
            <th>Usuario</th>
            <th>Email</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        <?php if(!empty($usuarios) && is_array($usuarios)): ?>
            <?php foreach($usuarios as $user): ?>
                <tr>
                    <td><?= $user['id'] ?></td>
                    <td><?= esc($user['usuario']) ?></td>
                    <td><?= esc($user['email']) ?></td>
                    <td>
                        <a href="<?= base_url('public/usuario/editar/'.$user['id']) ?>">Editar</a> | 
                        <a href="<?= base_url('public/usuario/eliminar/'.$user['id']) ?>" onclick="return confirm('¿Seguro que deseas eliminarlo?')">Eliminar</a>
                    </td>
                </tr>
            <?php endforeach; ?>
        <?php else: ?>
            <tr>
                <td colspan="4">No se encontraron usuarios registrados.</td>
            </tr>
        <?php endif; ?>
    </tbody>
</table>
