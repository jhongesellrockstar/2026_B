<?php $pager->setSurroundCount(2); ?>
<nav class="paginacion" aria-label="Paginación de fuentes">
<?php if ($pager->hasPreviousPage()): ?><a href="<?= $pager->getPreviousPage() ?>" rel="prev">Anterior</a><?php endif ?>
<?php foreach ($pager->links() as $link): ?>
<a href="<?= $link['uri'] ?>" <?= $link['active'] ? 'aria-current="page"' : '' ?>><?= $link['title'] ?></a>
<?php endforeach ?>
<?php if ($pager->hasNextPage()): ?><a href="<?= $pager->getNextPage() ?>" rel="next">Siguiente</a><?php endif ?>
</nav>
