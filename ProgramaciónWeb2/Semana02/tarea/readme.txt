## Enunciado del ejercicio

*"Formulario de registro de invitados con exportación a archivo"*

Desarrollar una aplicación en JavaScript (vanilla, sin frameworks) que permita registrar un evento y su lista de invitados, con la siguiente funcionalidad:

*1. Datos generales del evento*

El formulario debe incluir los siguientes campos:
- Nombre del evento (texto)
- Fecha (tipo date)
- Lugar (texto)

*2. Lista de invitados (dinámica)*

- Incluir un campo numérico ("Cantidad de invitados") que permita indicar cuántas personas se invitarán (mínimo 1, máximo 50).
- Al presionar el botón *"Agregar invitados", se deben generar dinámicamente *N bloques de inputs (uno por invitado), cada uno con:
  - Nombre completo
  - Correo electrónico
  - Teléfono
  - Relación con el anfitrión (select: familia, amigo, trabajo, otro)
- Los bloques deben numerarse (Invitado 1, Invitado 2, …).
- Permitir *eliminar* un bloque individual con un botón "✕" dentro de cada uno.

*3. Validación*

- Ningún campo puede quedar vacío antes de enviar.
- El correo debe tener formato válido.
- El teléfono debe tener al menos 8 dígitos.
- Mostrar un mensaje de error específico junto al campo que falle.

*4. Exportación a archivo .txt*

- Al presionar *"Guardar"*, los datos deben formatearse y descargarse como un archivo invitados.txt con este formato:


=== EVENTO: <nombre> ===
Fecha: <fecha>
Lugar: <lugar>
Total invitados: <N>

--- INVITADO 1 ---
Nombre: ...
Correo: ...
Teléfono: ...
Relación: ...

--- INVITADO 2 ---
...


- Usar Blob + URL.createObjectURL para generar la descarga sin servidor.

*5. Restricciones*

- No usar frameworks ni librerías externas.
- HTML, CSS y JS separados en archivos distintos.
- El CSS debe hacer que la interfaz sea responsiva y legible.
- Incluir comentarios en el código explicando las decisiones clave.

*Entregables:*
- index.html
- styles.css
- script.js
- Captura de pantalla del formulario con 3+ invitados generados y del archivo .txt descargado.