<div class="resumen"><strong><?= $pager->getTotal() ?> fuentes encontradas</strong><span>5 fuentes por página</span></div>
<p class="ayuda ayuda-tabla">Desliza la tabla para ver todas las columnas.</p>
<div class="tabla-contenedor"><table>
<caption class="solo-lector">Fuentes de datos hidroclimáticos</caption>
<thead><tr><th>ID</th><th>Nombre</th><th>Institución</th><th>Categoría</th><th>Variable principal</th><th>Cobertura</th><th>Acceso</th><th>Acciones</th></tr></thead>
<tbody>
<?php foreach ($fuentes as $fuente): ?>
<tr><td class="muted"><?= $fuente['id'] ?></td>
<td><a class="fuente-nombre" href="<?= site_url('fuentes/ver/' . $fuente['id']) ?>"><?= esc($fuente['nombre']) ?></a><?php if ($fuente['estado'] === 'Inactivo'): ?><small>Inactivo</small><?php endif ?></td>
<td><?= esc($fuente['institucion']) ?></td><td><span class="etiqueta"><?= esc($fuente['categoria']) ?></span></td>
<td><?= esc($fuente['variable'] ?? 'Sin especificar') ?></td><td><?= esc($fuente['cobertura']) ?></td><td><?= esc($fuente['tipo_acceso']) ?></td>
<td><div class="acciones"><a href="<?= site_url('fuentes/ver/' . $fuente['id']) ?>">Ver</a><a href="<?= site_url('fuentes/editar/' . $fuente['id']) ?>">Editar</a>
<form method="post" action="<?= site_url('fuentes/eliminar/' . $fuente['id']) ?>" class="eliminar"><?= csrf_field() ?><button class="enlace peligro" type="submit" aria-label="Eliminar <?= esc($fuente['nombre']) ?>">Eliminar</button></form></div></td></tr>
<?php endforeach ?>
<?php if (!$fuentes): ?><tr><td colspan="8" class="vacio">No se encontraron fuentes. Prueba con otro término o limpia los filtros.</td></tr><?php endif ?>
</tbody></table></div>
<?php // Ruta relativa a baseURL para evitar duplicar /clima_agua/public en los enlaces. ?>
<?= $pager->setPath('fuentes')->only(['q', 'categoria', 'ambito'])->links('default', 'catalogo') ?>
