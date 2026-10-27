# Segunda iteración visual · CLIMA Y AGUA — GARZA

## Identidad aplicada

Rojo Perú `#C8102E`, rojo oscuro `#8E0D22`, blanco `#FFFFFF`, fondo
`#F7F6F3`, borde `#DDD8D0`, grafito `#2D2D2D`, arena `#EDE7DC`,
verde humedal `#667A5B` y verde claro `#E7ECE3`.

Encabezado horizontal con garza y nombre; navbar roja con silueta blanca;
portada compacta con garza de 96 px; botones primarios rojos, secundarios
blancos; tabla con cabecera grafito, filas alternadas y hover arena;
formularios blancos con foco rojo; paginador activo rojo; footer grafito.
En móvil los filtros y formularios pasan a una columna y la tabla permite
desplazamiento horizontal, con una indicación visible.

## Logotipo

- Descargado: Heron Silhouette (NIH BioArt 851 - 797148).
- Fuente: Wikimedia Commons, original NIH BioArt / NIAID.
- Crédito: Courtesy of NIAID Ryan Kissinger.
- La ficha identifica la imagen como dominio público en Estados Unidos.
- Archivo: `public/assets/img/garza.svg`.
- Favicon: `public/favicon.svg`.
- Procedencia y adaptación: `public/assets/img/README_logo.txt`.
- Se preservó la geometría. `currentColor` permite cambiar el color mediante
  CSS al reutilizar el path con SVG/use; no se usan fotografías ni emojis.

Ficha: https://commons.wikimedia.org/wiki/File:Heron_Silhouette_(NIH_BioArt_851_-_797148).svg

## Archivos existentes modificados

1. `app/Views/template/header.php`: logo, identidad, favicon y versión de CSS.
2. `app/Views/template/navbar.php`: símbolo de la garza; los menús se conservan.
3. `app/Views/template/footer.php`: texto de catálogo demostrativo.
4. `app/Views/fuentes/index.php`: composición y texto de portada.
5. `app/Views/fuentes/tabla.php`: indicación para pantallas pequeñas y ajuste
   de enlaces del paginador a la ruta relativa `fuentes`.
6. `public/css/estilos.css`: paleta, tipografía, componentes y responsive.

El ajuste del paginador corrige un fallo previo observado al revisar las URLs:
los enlaces repetían `/clima_agua/public/`. Solo se corrigió la ruta generada
en la vista, sin cambiar paginate(5), parámetros, consulta ni número de filas.

## Funcionalidad conservada y comprobada

- Controller, Model, rutas, JavaScript y SQL tienen los mismos hashes que al
  inicio de esta iteración. No se cambió la consulta AJAX ni la validación.
- Las 15 fuentes iniciales conservan exactamente sus datos.
- El script existente `scripts/verificar.php` pasó: listado, crear, ver,
  editar, eliminar, búsqueda normal, AJAX, filtros y paginación.
- Las pruebas crean y eliminan un registro temporal, sin modificar los iniciales.
- En navegador: escribir preci actualiza la tabla sin recarga (4 fuentes).
- Oceanografía + Océano devuelve 4 fuentes; Siguiente en el catálogo completo
  muestra la segunda página y conserva 5 filas por página.
- Consola del navegador: sin errores JavaScript.
- Revisión visual en escritorio, tablet y móvil; SVG visible con color correcto.
- No se instalaron tecnologías ni herramientas nuevas. No se hizo git push.

## Capturas

- `capturas/01-listado.jpg`: catálogo en escritorio.
- `capturas/02-crear.jpg`: formulario de registro.
- `capturas/03-detalle.jpg`: detalle de PISCO.
- `capturas/04-movil.jpg`: catálogo en pantalla estrecha.

Las capturas muestran toda la página correspondiente; en móvil las columnas
restantes se consultan mediante el desplazamiento de la tabla.

URL de revisión: http://localhost/clima_agua/public/
