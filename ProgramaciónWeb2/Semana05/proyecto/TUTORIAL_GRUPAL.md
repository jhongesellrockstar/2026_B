# Tutorial grupal — Callao Limpio

Programación Web 2 · Ingeniería de Sistemas · Universidad Nacional del Callao · 2026-B.

## Acuerdo de estudio

Un solo proyecto React funcional, organizado en cinco responsabilidades. Cada estudiante domina su módulo y todos comprenden el flujo general. Este documento es una guía de estudio, no un discurso para memorizar. El video dura aproximadamente 40 minutos: explicar, abrir código, reconstruir un fragmento y demostrar su resultado.

El código revisado utiliza funciones, props, useState, useEffect, map, filter y un for para agrupar distritos. No requiere cambiar la arquitectura. Los puntos que necesitan explicación adicional son el inicializador de useState, la copia con ..., los condicionales ternarios y los estilos dinámicos; se estudian aquí sin reescribir la aplicación.

## Orden definitivo

| Tiempo del video | Integrante | Responsabilidad |
| --- | --- | --- |
| 00:00–08:00 | JOSÉ ALEJANDRO ANCALLA ALARCON | Inicio de React y estructura |
| 08:00–16:00 | DIEGO ENRIQUE CISNEROS AGURTO | Formulario y captura de datos |
| 16:00–24:00 | RODRIGO ALONSO BRINGAS MARTINEZ | Visualización de reportes |
| 24:00–32:00 | JESÚS THENEE SOTO SALDARRIAGA | Estado principal, acciones, filtros y persistencia |
| 32:00–40:00 | JHON GESELL VILLANUEVA PORTELLA | Estadísticas, gráficos e integración final |

## Mapa de componentes

```text
main.jsx
   │
   ▼
App.jsx
   ├── Header
   ├── Estadisticas
   ├── FormularioReporte
   ├── FiltroReportes
   ├── ListaReportes
   │       └── Reporte
   └── ResumenEstadistico
```

Este árbol expresa quién contiene a quién; no representa el orden de aparición en pantalla.

| Archivo o componente | Responsabilidad |
| --- | --- |
| main.jsx | Monta App en el elemento root de index.html. |
| App | Conserva reportes y filtro, define acciones y sincroniza el almacenamiento. |
| Header | Presenta el nombre y el contexto académico mediante JSX. |
| FormularioReporte | Controla los campos, valida y entrega un reporte nuevo a App. |
| ListaReportes | Recorre los reportes visibles o muestra un mensaje sin resultados. |
| Reporte | Presenta un objeto y botones que invocan las acciones recibidas. |
| FiltroReportes | Permite seleccionar qué estados se muestran en la lista. |
| Estadisticas | Cuenta todos los reportes, pendientes y atendidos. |
| ResumenEstadistico | Calcula porcentajes y cantidades por distrito y los representa con CSS. |

## Flujo que los cinco deben comprender

```text
Usuario
   │ escribe y envía
   ▼
FormularioReporte
   │ llama a la función recibida por props
   ▼
agregarReporte
   │
   ▼
App / estado reportes
   ├─────────────► localStorage (useEffect guarda texto JSON)
   ├─────────────► Estadisticas (array completo)
   ├─────────────► ResumenEstadistico (array completo)
   │ aplica el filtro de estado
   ▼
ListaReportes (reportesFiltrados + totalReportes)
   │ map
   ▼
Reporte
```

Al iniciar, recuperarReportes lee localStorage y proporciona el estado inicial a App. Al pulsar un botón de una tarjeta, la función recibida llama a eliminarReporte o cambiarEstado en App con el id. React vuelve a renderizar al actualizar el estado; los hijos reciben las nuevas props. El filtro selecciona una vista y no borra objetos. El resumen siempre usa todos los reportes.

## Módulo 1 — JOSÉ ALEJANDRO ANCALLA ALARCON

**Tiempo:** 8 minutos, 00:00–08:00.

**Estudiar:** React como biblioteca de interfaces; diferencia con manipular el DOM directamente; Vite; estructura; index.html; root; main.jsx; App; componentes; JSX; import y export. Entender superficialmente que App integra los componentes y conserva la lista.

**Abrir:** index.html, src/main.jsx, src/components/Header.jsx y src/App.jsx. Mostrar package.json solo para ubicar los comandos.

**Orden de explicación y práctica:**

1. 00:00–01:00: presentar problemática, curso y alcance: prototipo académico, sin vínculo oficial ni envío a autoridades.
2. 01:00–02:30: comparar getElementById/createElement con describir una interfaz a partir del estado; definir React y el papel de Vite.
3. 02:30–04:00: seguir index.html → root → main.jsx → App; mostrar imports.
4. 04:00–06:30: reconstruir un Header mínimo y explicar return, etiquetas JSX, className e interpolación.
5. 06:30–07:30: ubicar Header dentro de App y demostrar su título en el navegador.
6. 07:30–08:00: resumir la responsabilidad y dar paso al formulario.

**Fragmento que debe poder escribir** (versión mínima de estudio; el Header final contiene más textos):

```jsx
function Header() {
  return <h1>CALLAO LIMPIO</h1>;
}
export default Header;
```

Relacionarlo con el montaje real, sin tener que reescribir main.jsx completo:

```jsx
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

**Demostrar:** localizar el mismo root en HTML y JavaScript; guardar un cambio temporal de texto durante el ensayo y observar la actualización de Vite; restaurar el Header final.

**Preguntas del profesor:**

| Pregunta | Respuesta breve |
| --- | --- |
| ¿React es todo el sitio? | Es la biblioteca con la que construimos la interfaz; también usamos JavaScript, HTML y CSS. |
| ¿Qué hace Vite? | Sirve el proyecto en desarrollo y genera la compilación de producción. |
| ¿JSX es un archivo HTML? | Es sintaxis dentro de JavaScript que las herramientas transforman para construir la interfaz. |
| ¿Por qué el nombre Header comienza en mayúscula? | JSX distingue así un componente propio de una etiqueta HTML. |
| ¿Para qué está StrictMode? | Activa comprobaciones adicionales durante el desarrollo; puede repetir renderizados y efectos para detectar problemas. |

**Transición a Diego:** “App integra varios componentes. Ahora Diego mostrará uno de ellos: el formulario que captura los datos del reporte”.

## Módulo 2 — DIEGO ENRIQUE CISNEROS AGURTO

**Tiempo:** 8 minutos, 08:00–16:00.

**Conexión inicial:** “Ahora veremos uno de esos componentes: el formulario y su estado local”.

**Estudiar:** useState por campo y mensaje; value; onChange; formulario controlado; onSubmit; preventDefault; required y trim; objeto reporte; Date.now; props como funciones; limpieza de campos.

**Abrir:** src/components/FormularioReporte.jsx. Consultar la línea de App que entrega agregarReporte para ubicar al padre.

**Orden de explicación y práctica:**

1. 00:00–01:00 del bloque: identificar los cuatro campos y la función agregarReporte recibida.
2. 01:00–03:00: reconstruir un input controlado; seguir usuario → onChange → setUbicacion → nuevo renderizado.
3. 03:00–04:30: explicar onSubmit, preventDefault y las dos validaciones: required del navegador y trim en JavaScript.
4. 04:30–06:00: mostrar creación del objeto con estado Pendiente y llamada agregarReporte.
5. 06:00–07:30: registrar un ejemplo, comprobar limpieza y mensaje; probar espacios en blanco.
6. 07:30–08:00: conectar la captura con la visualización.

**Fragmento que debe escribir:** estas partes pertenecen al componente, la declaración antes del return y el JSX dentro del formulario.

```jsx
const [ubicacion, setUbicacion] = useState('');
```

```jsx
<input
  id="ubicacion"
  value={ubicacion}
  onChange={(event) => setUbicacion(event.target.value)}
  required
/>
```

**Demostrar también:** explicar el objeto final sin memorizar todos los select; el flujo submit → validar → crear objeto → agregarReporte → limpiar.

**Preguntas del profesor:**

| Pregunta | Respuesta breve |
| --- | --- |
| ¿Por qué value y onChange juntos? | El estado es la fuente del valor; onChange pide actualizarlo con lo escrito. |
| ¿Qué evita preventDefault? | El envío tradicional del formulario y la recarga de la página. |
| ¿Por qué trim si hay required? | required detecta vacío, pero una cadena de espacios necesita trim para esta validación. |
| ¿El formulario guarda en localStorage? | No; entrega el objeto a App y App se encarga de persistir el array. |
| ¿Date.now garantiza ids universales? | No; es una solución sencilla para este formulario manual, basada en milisegundos. |

**Transición a Rodrigo:** “Ya capturamos y entregamos el reporte. Rodrigo explicará cómo cada objeto aparece como una tarjeta”.

## Módulo 3 — RODRIGO ALONSO BRINGAS MARTINEZ

**Tiempo:** 8 minutos, 16:00–24:00.

**Conexión inicial:** “Una vez registrado el reporte, debemos representarlo mediante componentes”.

**Estudiar:** props; padre → hijo; array; map; key estable; Reporte; renderizado condicional; botones; diferencia entre datos y funciones; callbacks.

**Abrir:** src/components/ListaReportes.jsx y src/components/Reporte.jsx.

**Orden de explicación y práctica:**

1. 00:00–01:30: identificar props: reportes y totalReportes son datos; eliminarReporte y cambiarEstado son funciones.
2. 01:30–03:30: reconstruir el map y sus props; explicar que cada objeto produce una tarjeta y que key usa el id.
3. 03:30–05:00: recorrer Reporte: distrito, ubicación, tipo, descripción, estado y botones.
4. 05:00–06:30: explicar lista vacía frente a filtro sin resultados, usando totalReportes.
5. 06:30–07:30: demostrar tarjetas y seguir un clic hasta la función recibida.
6. 07:30–08:00: entregar el control del relato a App.

**Fragmento que debe escribir** (dentro del JSX de ListaReportes):

```jsx
{reportes.map((reporte) => (
  <Reporte
    key={reporte.id}
    reporte={reporte}
    eliminarReporte={eliminarReporte}
    cambiarEstado={cambiarEstado}
  />
))}
```

Relacionarlo con este botón dentro de Reporte:

```jsx
<button type="button" onClick={() => eliminarReporte(reporte.id)}>
  Eliminar
</button>
```

**Demostrar:** dos objetos producen dos tarjetas distintas; el botón envía el id del reporte correcto. No implementar la eliminación aquí: pertenece al módulo de Jesús.

**Preguntas del profesor:**

| Pregunta | Respuesta breve |
| --- | --- |
| ¿map modifica el array original? | No; devuelve un array nuevo, aquí de elementos JSX. |
| ¿Para qué sirve key? | Ayuda a React a identificar cada elemento entre renderizados; el id permanece estable al eliminar otros. |
| ¿key llega como prop normal a Reporte? | No; React la usa especialmente. El id está disponible dentro de reporte. |
| ¿Por qué la flecha en onClick? | Entrega una función para ejecutarla al pulsar, en vez de ejecutar eliminarReporte durante el renderizado. |
| ¿Las props se modifican desde el hijo? | No directamente; el hijo llama una función del padre para solicitar la actualización. |

**Transición a Jesús:** “La información que vimos en esas tarjetas se administra desde App. Jesús explicará sus acciones, filtros y almacenamiento”.

## Módulo 4 — JESÚS THENEE SOTO SALDARRIAGA

**Tiempo:** 8 minutos, 24:00–32:00.

**Conexión inicial:** “App conserva la información que usan las tarjetas y define qué ocurre al pulsar sus botones”.

**Estudiar:** estado reportes; inicializador recuperarReportes; agregar con ...; eliminar con filter; cambiar con map y copia del objeto; filtro; useEffect; localStorage; JSON.stringify/parse; errores de almacenamiento.

**Abrir:** src/App.jsx y src/components/FiltroReportes.jsx.

**Orden de explicación y práctica:**

1. 00:00–01:00: identificar estado principal y explicar useState(recuperarReportes): se pasa una función, sin llamarla en cada renderizado.
2. 01:00–03:00: reconstruir eliminarReporte; después recorrer agregarReporte y cambiarEstado, explicando las copias con ... y el ternario.
3. 03:00–04:30: explicar estado filtro y selección de reportesFiltrados; etiquetas plurales, valores internos Pendiente/Atendido.
4. 04:30–06:30: leer recuperarReportes y useEffect; distinguir lectura inicial, guardado al cambiar reportes y manejo de errores.
5. 06:30–07:30: eliminar un ejemplo, alternar filtros y recargar para comprobar persistencia.
6. 07:30–08:00: conectar el array completo con las estadísticas.

**Fragmento que debe escribir** (dentro de App):

```jsx
function eliminarReporte(id) {
  setReportes(reportes.filter((reporte) => reporte.id !== id));
}
```

**Qué debe demostrar y explicar:** filter conserva los objetos cuyo id es diferente; actualizar el estado provoca el renderizado y luego el efecto guarda. localStorage es una API del navegador, NO React.

La lectura inicial usa getItem y JSON.parse; valida que haya un array y campos esperados, y devuelve [] si no puede leer. El guardado usa JSON.stringify dentro de try/catch. La dependencia [reportes] sincroniza los cambios; no guarda el filtro. Los comentarios oxlint del efecto justifican informar el resultado del almacenamiento mediante errorGuardado, no cambian cómo funciona React.

**Preguntas del profesor:**

| Pregunta | Respuesta breve |
| --- | --- |
| ¿Eliminar y filtrar la pantalla son lo mismo? | No; eliminar cambia reportes. El filtro solo calcula la lista visible. |
| ¿Por qué usar ...? | Crea una copia nueva del array o del objeto, evitando modificar directamente el estado existente. |
| ¿Por qué recuperar antes del primer guardado? | Para no reemplazar datos guardados por una lista inicial vacía. |
| ¿Por qué stringify y parse? | localStorage guarda texto; stringify convierte a texto JSON y parse recupera valores JavaScript. |
| ¿Otro navegador verá esos datos? | No; dependen del navegador y del origen, incluida dirección y puerto. |
| ¿Qué pasa si el guardado falla? | App muestra un aviso; los cambios pueden perderse al recargar. |

**Transición a Jhon:** “Finalmente, con ese mismo array de reportes, Jhon calculará los indicadores y las visualizaciones y demostrará la aplicación completa”.

## Módulo 5 — JHON GESELL VILLANUEVA PORTELLA

**Tiempo:** 8 minutos, 32:00–40:00.

**Conexión inicial:** “Utilizando el mismo array de App calculamos nuestros indicadores y gráficos, sin guardar estadísticas adicionales”.

**Estudiar:** props reportes; length y filter; porcentajes; evitar división entre cero; for y objeto por distrito; Object.keys; Math.max; map; barras proporcionales; estilos dinámicos; conic-gradient; renderizado derivado del estado.

**Abrir:** src/components/Estadisticas.jsx, src/components/ResumenEstadistico.jsx y src/App.css. Mostrar en App las props reportes entregadas a ambos componentes.

**Orden de explicación y práctica:**

1. 00:00–01:00: relacionar props con estadísticas calculadas; distinguir array completo de lista filtrada.
2. 01:00–02:30: reconstruir total, pendientes, atendidos y porcentaje; explicar el caso cero.
3. 02:30–03:30: seguir el porcentaje hasta fondoCircular y style; señalar dimensiones y border-radius en CSS.
4. 03:30–04:30: explicar conteo por distrito, máximo y ancho proporcional de las barras.
5. 04:30–07:30: realizar la demostración integral indicada abajo.
6. 07:30–08:00: concluir conectando los cinco módulos y el alcance académico.

**Fragmento que debe escribir** (dentro del componente):

```jsx
const total = reportes.length;
const pendientes = reportes.filter((reporte) => reporte.estado === 'Pendiente').length;
const atendidos = reportes.filter((reporte) => reporte.estado === 'Atendido').length;
let porcentajePendientes = 0;
if (total > 0) {
  porcentajePendientes = pendientes / total * 100;
}
```

Mostrar cómo llega a la representación:

```jsx
let fondoCircular = '#e4e9e2';
if (total > 0) {
  fondoCircular = `conic-gradient(#c0923d 0% ${porcentajePendientes}%, #6c9b67 ${porcentajePendientes}% 100%)`;
}
```

```jsx
<div className="grafico-circular" style={{ background: fondoCircular }} aria-hidden="true" />
```

El elemento decorativo tiene aria-hidden porque las cantidades y porcentajes se leen en la leyenda textual. El CSS da al círculo anchura, altura y borde redondo. No utilizamos Chart.js, Recharts, D3 ni Plotly: solo React, JavaScript, JSX y CSS.

**Demostración final, ensayada para tres minutos:** partir de los ocho ejemplos (5 pendientes/3 atendidos; distritos 3/2/2/1). Registrar un noveno ejemplo temporal y localizar su tarjeta; marcarlo atendido; mostrar Pendientes y Atendidos; volver a Todos; eliminar solo el temporal; señalar total 8, círculo 62,5 %/37,5 % y barras Callao 3, Bellavista 2, Ventanilla 2, La Perla 1; recargar y comprobar los mismos datos. Los ejemplos se introducen siempre desde el formulario, nunca desde el código.

**Preguntas del profesor:**

| Pregunta | Respuesta breve |
| --- | --- |
| ¿Por qué no hay useState para las estadísticas? | Se derivan de reportes; guardarlas aparte duplicaría información que habría que sincronizar. |
| ¿Qué significa una barra al 100 %? | Es el distrito con más reportes, no necesariamente el 100 % del total. |
| ¿Cómo se calcula el ancho? | cantidad / mayorCantidad * 100; para 3/2/2/1 resulta 100 %, 66,7 %, 66,7 % y 33,3 %. |
| ¿Qué ocurre sin reportes? | Círculo neutro, cantidades cero y mensaje; no hay barras ni división entre cero. |
| ¿Cambiar el filtro altera el gráfico? | No: el gráfico recibe todos los reportes, no reportesFiltrados. |
| ¿Quién dibuja el gráfico? | JavaScript calcula; JSX crea elementos; CSS representa color y tamaño. |

**Transición de cierre:** “Los cinco módulos trabajan juntos en una sola aplicación: capturamos, administramos, mostramos y resumimos los reportes. Es un prototipo académico con persistencia local”.

## PREGUNTAS PARA TODO EL GRUPO

| Pregunta | Respuesta breve |
| --- | --- |
| ¿Qué es React? | Una biblioteca de JavaScript para construir interfaces mediante componentes. |
| ¿Qué es un componente? | En este proyecto, una función que devuelve JSX para una parte de la interfaz. |
| ¿Qué es JSX? | Sintaxis para describir la interfaz dentro de JavaScript, con expresiones entre llaves. |
| ¿Qué es useState? | Un hook que conserva un valor entre renderizados y proporciona una función para actualizarlo. |
| ¿Qué son las props? | Datos o funciones que un componente padre entrega a un hijo. |
| ¿Qué hace useEffect? | Sincroniza con sistemas externos después del renderizado; aquí guarda reportes en localStorage cuando cambian. |
| ¿Qué diferencia hay entre estado y props? | El componente conserva su estado; recibe props de su padre. |
| ¿Por qué React vuelve a renderizar? | Una actualización de estado puede provocar que recalcule la interfaz y sus hijos; actualiza el DOM según los cambios necesarios. |
| ¿Qué hace map()? | Devuelve un array con el resultado de transformar cada elemento. |
| ¿Qué hace filter()? | Devuelve un array con los elementos que cumplen una condición. |
| ¿Qué es localStorage? | Una API del navegador que guarda pares clave/valor de texto para un origen. |
| ¿Por qué usamos JSON.stringify? | Para convertir el array de objetos en texto que se pueda guardar. |
| ¿Por qué usamos JSON.parse? | Para convertir el texto JSON recuperado en valores de JavaScript. |
| ¿Qué aporta Vite? | Entorno de desarrollo con actualización de cambios y compilación para distribución. |
| ¿Por qué no utilizamos una base de datos? | El objetivo es practicar React básico; basta persistencia local y no existe un servicio compartido. |
| ¿Por qué es solamente un prototipo académico? | Sirve para aprendizaje; no está conectado a autoridades ni es un sistema oficial de gestión de residuos. |

## Criterio de preparación

Cada integrante debe explicar su fragmento sin leer línea por línea, predecir su resultado y responder dos preguntas de otro compañero. Todos deben recorrer el flujo completo con un ejemplo. Practiquen la reconstrucción con [PRACTICA_TUTORIAL.md](PRACTICA_TUTORIAL.md) y usen [GUIA_VIDEO.md](GUIA_VIDEO.md) para controlar el tiempo.

