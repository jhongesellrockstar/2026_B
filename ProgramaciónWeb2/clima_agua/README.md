# CLIMA Y AGUA · GARZA

Catálogo académico de fuentes de datos hidroclimáticos para Programación Web II,
Ingeniería de Sistemas, Universidad Nacional del Callao.

**Encuentra datos confiables para tu investigación.**

## Abrir la aplicación instalada

Iniciar Apache y MySQL en XAMPP y abrir **http://localhost/clima_agua/public/**.

Proyecto: `C:\xampp\htdocs\clima_agua`.
Base: `clima_agua_db`, cuatro tablas y 15 fuentes demostrativas.
No volver a importar SQL sobre la instalación existente.

## Requisitos

- Windows 11 y XAMPP con Apache, MySQL/MariaDB y phpMyAdmin.
- PHP 8.2 o posterior, con intl, mbstring y mysqli habilitadas.
- CodeIgniter 4.7.5, distribución manual oficial (carpeta `system`).
- Navegador moderno para fetch; la búsqueda normal funciona sin JavaScript.

Se comprobó PHP 8.2.12, Apache en 80, MySQL en 3306 y acceso local con root y
contraseña vacía. No se modificó ninguna base anterior. No se necesita Node.js,
Composer, Bootstrap ni librerías JavaScript.

## Instalación en otra copia de XAMPP

1. Copiar el proyecto en `C:\xampp\htdocs\clima_agua`.
2. Comprobar que existe `system\Boot.php`. La copia local incluye el framework.
   Git ignora `system`; si se obtiene desde Git, ejecutar en la carpeta:
   `powershell -ExecutionPolicy Bypass -File .\instalar_framework.ps1`.
   Descarga solamente CodeIgniter oficial 4.7.5 y copia `system`.
3. Iniciar Apache y MySQL desde XAMPP.
4. Abrir `http://localhost/phpmyadmin/`, Importar, seleccionar
   `database/clima_agua_db.sql` y ejecutar. Crea la base, tablas y datos.
   Importar una sola vez sobre una base nueva; no elimina tablas existentes.
5. Copiar `.env.example` como `.env` si no existe. Verificar primero las
   credenciales y el puerto real de MySQL. La configuración local comprobada es:

```ini
CI_ENVIRONMENT = development
app.baseURL = 'http://localhost/clima_agua/public/'
app.indexPage = ''
database.default.hostname = localhost
database.default.database = clima_agua_db
database.default.username = root
database.default.password = ''
database.default.DBDriver = MySQLi
database.default.port = 3306
```

6. Abrir exactamente **http://localhost/clima_agua/public/**.
   Apache debe permitir `.htaccess` y tener `mod_rewrite`, como el XAMPP
   verificado. Si Apache usa otro puerto, ajustar `app.baseURL`.
   `writable` debe permitir escritura para las sesiones y registros.

El `.htaccess` de la raíz permite servir solo `public`; bloquea los demás
directorios. No mover `index.php` a la raíz. El entorno development se usa
para la exposición local. No se ha publicado el proyecto en Internet.

## Funcionalidades y base de datos

- CRUD de Fuentes: registrar, listar, ver, editar y eliminar mediante POST y CSRF.
- Búsqueda normal por nombre, institución y cobertura; también variable y
  descripción para que “preci” encuentre Precipitación.
- AJAX con fetch, pausa de 300 ms y cancelación de solicitudes anteriores.
- Filtros por categoría y ámbito físico, combinables con búsqueda y paginación.
- Paginador nativo de CodeIgniter con `paginate(5)`.
- Variables y Categorías son listas de referencia; el CRUD principal es Fuentes.
- HTML escapado, URL limitada a http/https y confirmación JavaScript al eliminar.

Tablas: `fuentes`, `variables`, `categorias`, `ambitos`. Se añadió `variable_id`
a fuentes para representar una variable principal sin crear una quinta tabla.
Los portales con muchos productos usan “Varias variables”. Las relaciones
están protegidas por claves foráneas.

Ámbito significa Río, Lago, Océano, Atmósfera o Cuenca hidrográfica.
La procedencia nacional/internacional se indica en Cobertura e Institución.
Activo/Inactivo describe el registro: ambos estados aparecen en el catálogo.

Los 15 registros son demostrativos. Resolución espacial, resolución temporal,
periodo, formato y acceso quedan “Por verificar”. Las condiciones varían según
producto: consultar la documentación oficial antes de investigar. RAIN4PE
conserva URL vacía hasta verificar su publicación original.

Referencias de orientación, sin copiar textos:

- [CodeIgniter: instalación](https://codeigniter.com/user_guide/installation/)
- [CodeIgniter: requisitos](https://codeigniter.com/user_guide/intro/requirements.html)
- [CHIRPS, CHC](https://www.chc.ucsb.edu/data/chirps3)
- [GPM, NASA](https://gpm.nasa.gov/data/directory)
- [ERA5, ECMWF](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5)
- [W3Schools: fetch](https://www.w3schools.com/js/js_api_fetch.asp)

## Archivos para estudiar, en orden

1. `app/Config/Routes.php`: URL, método HTTP y Controller.
2. `app/Controllers/Fuentes.php`: listado, validación, CRUD y `buscarAjax`.
3. `app/Models/FuenteModel.php`: JOIN, LIKE, filtros y campos permitidos.
4. `app/Views/fuentes/index.php`: buscador y contenedor de resultados.
5. `app/Views/fuentes/tabla.php`: foreach, acciones y paginador nativo.
6. `public/js/fuentes.js`: input, fetch y actualización de HTML.
7. `app/Views/fuentes/formulario.php`: campos compartidos por crear y editar.
8. `app/Views/fuentes/ver.php`: ficha de la fuente.
9. `app/Views/template/header.php`, `navbar.php`, `footer.php`: templates.
10. `database/clima_agua_db.sql`: estructura, relaciones y datos iniciales.

```text
Usuario escribe -> input -> fetch /fuentes/buscar?q=preci
-> Fuentes::buscarAjax -> FuenteModel::catalogo -> MySQL
-> view fuentes/tabla -> HTML parcial -> resultados.innerHTML
```

El Controller devuelve solo tabla y paginador. El botón Buscar envía GET normal.
Los enlaces del paginador apuntan al listado completo; JavaScript puede
interceptarlos para actualizar solo la tabla. Los filtros se conservan en GET.
No se consumen APIs ni se descargan o procesan datos científicos.

## Verificación

Prueba reproducible con Apache y MySQL iniciados (crea y elimina un registro
temporal; no modifica las 15 fuentes iniciales):

```powershell
C:\xampp\php\php.exe C:\xampp\htdocs\clima_agua\scripts\verificar.php
```

Comprueba listado, MySQL, cinco filas, página 2, búsqueda normal, parcial AJAX,
filtros con paginación, cero resultados, catálogos, detalle, formularios, CRUD,
validación, escape de HTML, rechazo de GET al eliminar y bloqueo de `.env`.
La revisión del navegador comprueba búsquedas dinámicas y errores JavaScript.
Consultar `VERIFICACION.md` y el guion `GUIA_VIDEO.txt`.

CodeIgniter conserva su licencia MIT en `LICENSE`. Su documentación original
está en `README_FRAMEWORK.md`. El código que corresponde estudiar está en
`app`, `public/js`, `public/css` y `database`.
