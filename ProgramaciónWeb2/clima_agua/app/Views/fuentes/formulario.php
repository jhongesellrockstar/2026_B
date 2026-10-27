<?php if ($errores = session()->getFlashdata('errores')): ?>
<div class="aviso error" role="alert"><strong>Revisa los campos:</strong><ul><?php foreach ($errores as $error): ?><li><?= esc($error) ?></li><?php endforeach ?></ul></div>
<?php endif ?>
<p class="ayuda">Los campos con * son obligatorios. Si un dato científico no está verificado, indica “Por verificar”.</p>
<form action="<?= esc($accion) ?>" method="post">
<?= csrf_field() ?>
<div class="formulario">
<?php foreach (['nombre' => 'Nombre', 'institucion' => 'Institución'] as $campo => $label): ?>
<label><?= $label ?> *<input name="<?= $campo ?>" value="<?= esc(old($campo, $fuente[$campo] ?? ''), 'attr') ?>" required maxlength="<?= $campo === 'nombre' ? 150 : 200 ?>"></label>
<?php endforeach ?>
<label class="ancho">Descripción<textarea name="descripcion" rows="3" maxlength="5000"><?= esc(old('descripcion', $fuente['descripcion'] ?? '')) ?></textarea></label>
<?php foreach (['categoria_id' => ['Categoría', $categorias], 'ambito_id' => ['Ámbito', $ambitos], 'variable_id' => ['Variable principal', $variables]] as $campo => $opcion): ?>
<label><?= $opcion[0] ?> *<select name="<?= $campo ?>" required><option value="">Selecciona una opción</option>
<?php foreach ($opcion[1] as $item): ?><option value="<?= $item['id'] ?>" <?= (string) old($campo, $fuente[$campo] ?? '') === (string) $item['id'] ? 'selected' : '' ?>><?= esc($item['nombre']) ?></option><?php endforeach ?>
</select></label>
<?php endforeach ?>
<?php foreach (['cobertura' => 'Cobertura', 'resolucion_espacial' => 'Resolución espacial', 'resolucion_temporal' => 'Resolución temporal', 'periodo_disponible' => 'Periodo disponible', 'formato' => 'Formato'] as $campo => $label): ?>
<label><?= $label ?><input name="<?= $campo ?>" value="<?= esc(old($campo, $fuente[$campo] ?? ''), 'attr') ?>" maxlength="200"></label>
<?php endforeach ?>
<label>Tipo de acceso *<select name="tipo_acceso" required><?php foreach (['Libre','Registro requerido','Solicitud institucional','Por verificar'] as $item): ?><option <?= old('tipo_acceso', $fuente['tipo_acceso'] ?? 'Por verificar') === $item ? 'selected' : '' ?>><?= esc($item) ?></option><?php endforeach ?></select></label>
<label>Estado *<select name="estado" required><?php foreach (['Activo','Inactivo'] as $item): ?><option <?= old('estado', $fuente['estado'] ?? 'Activo') === $item ? 'selected' : '' ?>><?= $item ?></option><?php endforeach ?></select></label>
<label class="ancho">URL oficial<input type="url" name="url" placeholder="https://" maxlength="500" value="<?= esc(old('url', $fuente['url'] ?? ''), 'attr') ?>"></label>
</div><div class="botones"><button type="submit">Guardar fuente</button><a class="boton secundario" href="<?= site_url('fuentes') ?>">Cancelar</a></div>
</form>
