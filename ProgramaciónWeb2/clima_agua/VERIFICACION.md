# Verificación local

Entorno: Windows, Apache XAMPP puerto 80, PHP 8.2.12,
MySQL/MariaDB puerto 3306, CodeIgniter 4.7.5.

- Apache: HTTP 200 en `/clima_agua/public/`.
- MySQL: `clima_agua_db`, cuatro tablas, 15 fuentes iniciales.
- Sintaxis de los archivos PHP de `app`: correcta.
- CRUD: registro temporal creado, consultado, editado y eliminado por HTTP.
- URL vacía aceptada. Nombre vacío y URL javascript rechazados.
- Búsqueda normal NASA: GPM y NASA Earthdata.
- AJAX preci: PISCO, CHIRPS, GPM y RAIN4PE; HTML parcial.
- Filtros Oceanografía + Océano con segunda página: IMARPE.
- Cinco filas por página, tres páginas iniciales, conservación de filtros.
- Cero resultados: mensaje claro.
- Variables, Categorías, Ver, Crear y Editar: HTTP 200.
- ID inexistente: HTTP 404. Eliminar por GET: HTTP 404.
- CSRF habilitado, HTML escapado, `.env` bloqueado con HTTP 403.
- Navegador: preci y NASA dinámicos comprobados; sin errores JS.
- Navegador: Siguiente y Anterior actualizan la tabla por AJAX.

La herramienta de navegador se bloqueó al abrir la confirmación JavaScript de
eliminación, por lo que no se completó la comprobación interactiva de ese diálogo.
El código incluye confirm() y la eliminación sí pasó por HTTP con un registro
temporal. Si queda un diálogo de prueba visible, pulsar Cancelar o Escape.
La prueba de POST sin CSRF genera deliberadamente una SecurityException en el
log: corresponde al rechazo esperado del formulario sin token.

Los registros temporales se eliminaron. Se conservan 15 fuentes iniciales.
No se verificó científicamente cada producto: son registros demostrativos,
con las características específicas pendientes indicadas como Por verificar.

Repetir: `C:\xampp\php\php.exe scripts\verificar.php`.
