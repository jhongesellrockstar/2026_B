<?php
// Ejecutar solo por consola: C:\xampp\php\php.exe scripts\verificar.php
if (PHP_SAPI !== 'cli') exit('Solo consola.');
$base = 'http://localhost/clima_agua/public/';
$cookie = tempnam(sys_get_temp_dir(), 'clima-test-');
$id = null;

function solicitar(string $ruta, ?array $datos = null): array
{
    global $base, $cookie;
    $ch = curl_init($base . $ruta);
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_COOKIEJAR => $cookie,
        CURLOPT_COOKIEFILE => $cookie, CURLOPT_TIMEOUT => 20]);
    if ($datos !== null) {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($datos));
    }
    $html = curl_exec($ch);
    if ($html === false) throw new RuntimeException(curl_error($ch));
    $estado = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    return [$estado, $html];
}
function comprobar(bool $condicion, string $mensaje): void
{
    if (!$condicion) throw new RuntimeException('FALLO: ' . $mensaje);
    echo 'OK: ' . $mensaje . PHP_EOL;
}
function token(string $html): array
{
    preg_match('/name="(csrf_[^"]+)" value="([^"]+)"/', $html, $m);
    if (!$m) throw new RuntimeException('No se encontro el token CSRF.');
    return [$m[1] => $m[2]];
}

try {
    [$estado, $html] = solicitar('fuentes');
    comprobar($estado === 200 && str_contains($html, 'PISCO'), 'Apache, MySQL y listado');
    preg_match('/<tbody>(.*?)<\/tbody>/s', $html, $tabla);
    comprobar(substr_count($tabla[1], '<tr>') === 5, 'Cinco fuentes por pagina');
    [$estado, $html] = solicitar('fuentes?page=2');
    comprobar($estado === 200 && str_contains($html, 'Copernicus Marine') && !str_contains($html, '>PISCO<'), 'Segunda pagina');
    [, $html] = solicitar('fuentes?q=NASA');
    comprobar(str_contains($html, 'GPM') && str_contains($html, 'NASA Earthdata') && !str_contains($html, '>PISCO<'), 'Busqueda normal por institucion');
    [, $html] = solicitar('fuentes/buscar?q=preci');
    comprobar(str_contains($html, '>PISCO<') && str_contains($html, '>CHIRPS<') && !str_contains($html, '<html'), 'AJAX devuelve HTML parcial de precipitacion');
    [, $html] = solicitar('fuentes/buscar?categoria=3&ambito=4&page=2');
    comprobar(str_contains($html, 'IMARPE') && str_contains($html, 'categoria=3') && str_contains($html, 'ambito=4'), 'Filtros y paginacion combinados');
    [, $html] = solicitar('fuentes/buscar?q=ZZZ_SIN_RESULTADOS');
    comprobar(str_contains($html, 'No se encontraron fuentes'), 'Estado sin resultados');
    foreach (['variables', 'categorias', 'fuentes/ver/1', 'fuentes/editar/1', 'fuentes/crear'] as $ruta) {
        [$estado] = solicitar($ruta);
        comprobar($estado === 200, $ruta);
    }
    [, $html] = solicitar('fuentes/crear');
    $csrf = token($html);
    $datos = ['nombre' => 'PRUEBA_' . uniqid(), 'institucion' => 'UNAC', 'descripcion' => '<script>alert(1)</script>',
        'categoria_id' => '1', 'ambito_id' => '5', 'variable_id' => '1', 'cobertura' => 'Prueba local',
        'resolucion_espacial' => '', 'resolucion_temporal' => '', 'periodo_disponible' => '',
        'formato' => '', 'tipo_acceso' => 'Libre', 'url' => '', 'estado' => 'Activo'];
    [$estado] = solicitar('fuentes/guardar', array_merge($datos, $csrf));
    comprobar($estado === 303 || $estado === 302, 'CREATE acepta URL vacia');
    [, $html] = solicitar('fuentes?q=' . $datos['nombre']);
    preg_match('~/fuentes/ver/(\d+)~', $html, $m);
    comprobar(isset($m[1]), 'Registro persistido en MySQL');
    $id = (int) $m[1];
    [, $html] = solicitar('fuentes/ver/' . $id);
    comprobar(str_contains($html, '&lt;script&gt;') && !str_contains($html, '<script>alert'), 'READ escapa contenido HTML');
    $datos['nombre'] .= '_EDITADO';
    $datos['estado'] = 'Inactivo';
    [$estado] = solicitar('fuentes/actualizar/' . $id, array_merge($datos, $csrf));
    [, $html] = solicitar('fuentes/ver/' . $id);
    comprobar(str_contains($html, $datos['nombre']) && str_contains($html, 'Inactivo'), 'UPDATE persistido');
    $invalidos = $datos;
    $invalidos['nombre'] = '';
    $invalidos['url'] = 'javascript:alert(1)';
    solicitar('fuentes/actualizar/' . $id, array_merge($invalidos, $csrf));
    [, $html] = solicitar('fuentes/editar/' . $id);
    comprobar(str_contains($html, 'Revisa los campos'), 'Validacion del servidor y errores');
    [$estado] = solicitar('fuentes/eliminar/' . $id);
    comprobar($estado === 404, 'GET no puede eliminar');
    [$estado] = solicitar('fuentes/eliminar/' . $id, $csrf);
    [$lectura] = solicitar('fuentes/ver/' . $id);
    comprobar(($estado === 303 || $estado === 302) && $lectura === 404, 'DELETE persistido y detalle inexistente 404');
    $id = null;
    [$estado] = solicitar('fuentes/guardar', $datos);
    [, $html] = solicitar('fuentes?q=' . $datos['nombre']);
    comprobar(str_contains($html, 'No se encontraron fuentes'), 'POST sin CSRF no crea registros');
    [$estado] = solicitar('../.env');
    comprobar($estado === 403, '.env protegido por Apache');
    echo 'Verificacion completa. El registro temporal fue eliminado.' . PHP_EOL;
} finally {
    if ($id !== null) solicitar('fuentes/eliminar/' . $id, $csrf);
    unlink($cookie);
}
