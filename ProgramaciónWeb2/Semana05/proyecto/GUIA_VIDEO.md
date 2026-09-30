# Guía para el video — Callao Limpio

Programación Web 2 · Ingeniería de Sistemas · Universidad Nacional del Callao · 2026-B.

Duración total aproximada: **40 minutos**, distribuidos en **8 minutos por estudiante**. Los cinco explican, muestran código y reconstruyen un fragmento en tiempo real. Mantener un solo proyecto funcional. Esta guía organiza la grabación; TUTORIAL_GRUPAL.md desarrolla los conceptos y preguntas, y PRACTICA_TUTORIAL.md contiene los ejercicios.

## Orden definitivo de grabación

| Tiempo | Integrante | Explicación, escritura y demostración |
| --- | --- | --- |
| 00:00–08:00 | JOSÉ ALEJANDRO ANCALLA ALARCON | Problemática y alcance académico; React frente al DOM manual; Vite; index.html, root, main.jsx y App. Reconstruir un Header sencillo y explicar componentes, JSX e imports. |
| 08:00–16:00 | DIEGO ENRIQUE CISNEROS AGURTO | FormularioReporte.jsx: useState, value/onChange, onSubmit, preventDefault, required, trim, objeto con Date.now, props y limpieza. Reconstruir un input controlado y demostrar un envío. |
| 16:00–24:00 | RODRIGO ALONSO BRINGAS MARTINEZ | ListaReportes.jsx y Reporte.jsx: props de datos y funciones, map, key, renderizado condicional y botones. Reconstruir el recorrido que produce tarjetas y seguir un clic. |
| 24:00–32:00 | JESÚS THENEE SOTO SALDARRIAGA | App.jsx y FiltroReportes.jsx: array principal, agregar, eliminar, cambiar estado, filtros, lectura inicial, useEffect y localStorage. Reconstruir eliminarReporte y explicar el guardado JSON. |
| 32:00–40:00 | JHON GESELL VILLANUEVA PORTELLA | Estadisticas.jsx, ResumenEstadistico.jsx y App.css: indicadores derivados, porcentajes, conteo por distrito, barras y conic-gradient. Reconstruir cálculo representativo, seguirlo hasta CSS y realizar la demostración integral y conclusión. |

En los primeros cuatro bloques, reservar unos dos minutos para escribir y al menos un minuto para mostrar resultados. Jhon dedica 4:30 a explicación y reconstrucción, 3:00 a la demostración y 0:30 al cierre. Las transiciones forman parte de los ocho minutos, no son bloques adicionales.

## Transiciones para un relato continuo

- José → Diego: “App integra componentes. Ahora veremos el formulario que captura los datos”.
- Diego → Rodrigo: “Una vez registrado el reporte debemos representarlo en pantalla”.
- Rodrigo → Jesús: “La información que vimos en esas tarjetas se administra desde App”.
- Jesús → Jhon: “Con ese mismo array de reportes calculamos nuestros indicadores y visualizaciones”.
- Jhon cierra explicando cómo los cinco módulos colaboran en una sola aplicación.

Usar estas ideas con palabras propias; no memorizar un discurso ni leer cada línea.

## Preparación

1. En otro equipo, ejecutar npm install; iniciar con npm run dev y abrir la dirección indicada.
2. Mantener la misma dirección y puerto: localhost y 127.0.0.1 no comparten localStorage.
3. Tener abiertos los archivos de cada módulo, el navegador y los documentos de estudio.
4. Ensayar reconstrucciones parciales según PRACTICA_TUTORIAL.md; restaurar los bloques originales antes de pasar a la siguiente parte.
5. Preparar desde el formulario ocho ejemplos: Callao 3, Bellavista 2, Ventanilla 2 y La Perla 1; dejar 5 pendientes y 3 atendidos. No guardar ejemplos en el código.
6. Revisar legibilidad del editor y audio; cronometrar las cinco participaciones con escritura incluida.
7. No atribuir el sistema a la UNAC, municipalidad ni gobierno regional. Es un prototipo académico y no envía reportes a autoridades.

## Demostración integral — Jhon

1. Registrar un ejemplo temporal y localizarlo en la lista: el total pasa de 8 a 9.
2. Marcarlo atendido y observar el cambio del estado y del círculo.
3. Mostrar Pendientes y Atendidos; explicar que las estadísticas siguen contando todos los reportes.
4. Volver a Todos y eliminar únicamente el ejemplo temporal: debe desaparecer y el total volver a 8.
5. Mostrar 5 pendientes y 3 atendidos: 62,5 % y 37,5 %; barras por distrito 3/2/2/1.
6. Recargar en la misma dirección y confirmar que los datos permanecen.
7. Concluir: componentes, estado, props, eventos y persistencia local trabajando juntos; una solución real compartida necesitaría servicios fuera del alcance del curso.

La vuelta a pendiente se demuestra en la parte de acciones de Jesús. La validación del formulario se demuestra con Diego. Así el recorrido final conecta conceptos sin consumir el tiempo de explicación de los gráficos.

## Puntos que no deben faltar

- Antes se manipulaba el DOM directamente; aquí se cambia el estado y React actualiza la interfaz.
- App conserva la lista; los hijos reciben datos y funciones mediante props.
- Las estadísticas se calculan, no se guardan por separado.
- localStorage es una API del navegador, no React. useEffect sincroniza el array con ese almacenamiento.
- ResumenEstadistico.jsx recibe reportes por props. JavaScript calcula y CSS representa; no usamos Chart.js, Recharts, D3 ni Plotly.
- filter cuenta estados; cantidad / total * 100 da los porcentajes evitando dividir entre cero.
- conic-gradient pinta el círculo; sin reportes, se usa un color neutro.
- Un for cuenta distritos; Object.keys obtiene nombres y map genera barras. El ancho se compara con el distrito más numeroso, no con el total.
- No existe estado adicional para gráficos: cambiar reportes provoca un nuevo renderizado.

## Preguntas previsibles

| Pregunta | Respuesta breve |
| --- | --- |
| ¿Por qué no usamos fetch? | No hay API ni backend; localStorage cubre la persistencia del prototipo. |
| ¿Qué pasa al recargar? | El inicializador de useState lee los reportes guardados; el filtro vuelve a Todos. |
| ¿Por qué copiar con ...? | Para crear un array u objeto nuevo sin modificar directamente el estado anterior. |
| ¿Qué diferencia hay entre props y estado? | El componente conserva su estado y recibe props del padre. |
| ¿Por qué Date.now? | Es un identificador sencillo para el formulario manual; no garantiza unicidad en un sistema distribuido. |
| ¿Atendido significa que intervino una autoridad? | No: el usuario marca manualmente un estado del prototipo. |

Todos deben estudiar también las preguntas comunes y el flujo completo en TUTORIAL_GRUPAL.md. Cada integrante profundiza en su módulo; no se exige memorizar todos los archivos.
