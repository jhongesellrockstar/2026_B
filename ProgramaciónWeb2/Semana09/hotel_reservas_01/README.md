# Sistema de Reserva de Habitaciones

**Curso:** Programación Web II · Ingeniería de Sistemas · Universidad Nacional del Callao.

CRUD académico con PHP, CodeIgniter **4.7.5**, MySQL/MariaDB, XAMPP, HTML y CSS propio. JavaScript únicamente muestra una ayuda visual del precio y capacidad; la regla definitiva está en PHP. Sin AJAX ni librerías frontend.

## Ejecutar esta instalación

1. Abrir XAMPP y encender **Apache** y **MySQL**.
2. Abrir **http://localhost/hotel_reservas_01/public/** o ejecutar `ABRIR_PROYECTO.cmd`.

Proyecto: `C:\xampp\htdocs\hotel_reservas_01`.
BD: `hotel_reservas_01`, ya preparada con tres ejemplos. No necesita login ni Spark Serve.

## Instalar otra copia

1. Usar XAMPP con PHP 8.2 o superior y extensiones intl, mbstring y mysqli.
2. Copiar la carpeta completa dentro de `C:\xampp\htdocs`, con nombre `hotel_reservas_01`.
3. Encender Apache y MySQL. Crear la BD `hotel_reservas_01` en phpMyAdmin.
4. Importar `database/hotel_reservas_01.sql` desde phpMyAdmin, **o**, con `.env` configurado según el paso siguiente, ejecutar desde la raíz del proyecto:

```powershell
& C:\xampp\php\php.exe spark migrate
& C:\xampp\php\php.exe spark db:seed HabitacionesSeeder
```

5. Revisar `.env`; si no existe, copiar `.env.example` con ese nombre, sin extensión `.txt`. Debe indicar baseURL `http://localhost/hotel_reservas_01/public/`, host `localhost`, BD `hotel_reservas_01`, usuario `root`, driver `MySQLi` y puerto `3306`. Ajustar la contraseña según la instalación local.
6. Abrir la URL indicada. El framework y sus dependencias ya están incluidos; no es necesario Composer para usar esta copia.

Elegir SQL o migración más seeder. La migración está en la ubicación real de CodeIgniter: **app/Database/Migrations**. `migrations` es su tabla técnica de seguimiento. El SQL incluye estructura y ejemplos; no modifica el proyecto maestro ni su base de datos.

## Código del ejercicio

- `app/Models/HabitacionModel.php`: tabla, clave primaria y campos permitidos.
- `app/Controllers/Habitaciones.php`: index, crear, guardar, editar, actualizar y eliminar.
- `app/Config/Routes.php`: siete rutas GET/POST explícitas.
- `app/Database/Migrations/2026-10-27-000001_CrearHabitaciones.php`: estructura de habitaciones.
- `app/Database/Seeds/HabitacionesSeeder.php`: tres datos de instalación.
- `app/Views/habitaciones`: listado y formularios Crear/Editar.
- `app/Views/templates`: cabecera, mensajes y pie comunes.
- `public/css/estilos.css` y `public/js/habitaciones.js`: presentación y vista previa local.

`system`, `spark`, `public/index.php` y la configuración estándar pertenecen a la base de CodeIgniter. No se reescribieron sus archivos internos. Sólo se habilitó CSRF y se omitió la barra de depuración para presentar el ejercicio.

| Tipo | Capacidad | Precio por noche |
|---|---:|---:|
| sencilla | 1 | S/ 100.00 |
| doble | 2 | S/ 200.00 |
| triple | 3 | S/ 300.00 |

Estados: disponible, mantenimiento y ocupada. Código requerido y único, de hasta 20 caracteres. Tipo, estado y fecha se validan en PHP. Editar recalcula la tarifa; Eliminar utiliza POST con confirmación. La fecha se almacena como DATE.

## Estudiar y demostrar

Leer `GUIA_ESTUDIO.txt` y `GUION_VIDEO.txt`. Crear HAB-010 como Doble y Disponible; comprobar 2 huéspedes y S/ 200; editar a Ocupada; actualizar; eliminar y confirmar. Conservar H101, H102 y H103.

`ABRIR_CODIGO.cmd` abre esta carpeta con `code .` si VS Code está disponible. Los accesos no inician servicios ni cierran procesos.

## Comprobar

```powershell
& C:\xampp\php\php.exe spark routes
& C:\xampp\php\php.exe spark migrate:status
Get-ChildItem app -Filter *.php -Recurse | ForEach-Object { & C:\xampp\php\php.exe -l $_.FullName }
```

Las pruebas HTTP de desarrollo están en `tests/probar_crud.py` y sus resultados en `writable/pruebas_crud.json`. Python sólo se utilizó como herramienta de prueba; no se necesita para ejecutar la aplicación. La prueba crea registros temporales y los elimina al terminar.

Si localhost no abre, revisar Apache. Ante un error de conexión, revisar MySQL y `.env`. Si faltan tablas, importar el SQL o ejecutar la migración. Para un 404, comprobar que la URL termina en `/public/` y que la carpeta no está duplicada.
