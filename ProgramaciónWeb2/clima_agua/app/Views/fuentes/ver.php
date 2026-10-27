<?= view('template/header') ?>
<a class="volver" href="<?= site_url('fuentes') ?>">← Volver al catálogo</a>
<section class="panel"><p class="sobrelinea"><?= esc($fuente['categoria']) ?> · <?= esc($fuente['ambito']) ?></p>
<h1><?= esc($fuente['nombre']) ?></h1><p><?= esc($fuente['descripcion']) ?></p>
<dl class="detalle">
<?php foreach (['institucion' => 'Institución', 'variable' => 'Variable principal', 'cobertura' => 'Cobertura', 'resolucion_espacial' => 'Resolución espacial', 'resolucion_temporal' => 'Resolución temporal', 'periodo_disponible' => 'Periodo disponible', 'formato' => 'Formato', 'tipo_acceso' => 'Tipo de acceso', 'estado' => 'Estado', 'created_at' => 'Registrado', 'updated_at' => 'Actualizado'] as $campo => $label): ?>
<div><dt><?= $label ?></dt><dd><?= esc($fuente[$campo] ?: 'Sin especificar') ?></dd></div>
<?php endforeach ?>
</dl><div class="botones">
<?php if ($fuente['url'] && in_array(strtolower(parse_url($fuente['url'], PHP_URL_SCHEME) ?? ''), ['http','https'], true)): ?>
<a class="boton" href="<?= esc($fuente['url'], 'attr') ?>" target="_blank" rel="noopener noreferrer">Visitar fuente oficial ↗</a><?php endif ?>
<a class="boton secundario" href="<?= site_url('fuentes/editar/' . $fuente['id']) ?>">Editar fuente</a></div>
<p class="ayuda">Registro demostrativo. Verifica las condiciones y especificaciones en la documentación oficial.</p></section>
<?= view('template/footer') ?>
