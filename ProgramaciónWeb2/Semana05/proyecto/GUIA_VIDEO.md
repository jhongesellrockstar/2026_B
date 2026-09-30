# Guía para el video — Callao Limpio

Duración sugerida: 8 a 10 minutos. Cada integrante puede presentar varias partes. Practiquen con la aplicación abierta y el código al lado.

| Parte | Qué explicar | Qué mostrar |
| --- | --- | --- |
| 1. Problemática (40 s) | La acumulación de residuos en Lima y Callao motiva un registro sencillo. Es un prototipo académico; no envía denuncias ni representa a autoridades. | Cabecera de la aplicación. |
| 2. Qué es React (40 s) | React es una biblioteca de JavaScript para construir interfaces con componentes. Aunque el curso agrupa herramientas como frameworks, React se describe como biblioteca. Al cambiar el estado, actualiza la interfaz. | src/main.jsx y App.jsx. |
| 3. Estructura (30 s) | Vite inicia el entorno. main monta App; components divide la pantalla. | Árbol de src y comandos del README. |
| 4. Componentes (40 s) | Una función devuelve JSX. Header presenta el nombre; Estadisticas calcula cantidades a partir de reportes. | Header.jsx y Estadisticas.jsx. |
| 5. Formulario y useState (60 s) | Cada campo tiene estado local. value muestra su valor y onChange lo actualiza. onSubmit evita recargar, valida campos con trim, crea el objeto y limpia. | FormularioReporte.jsx. |
| 6. Props y comunicación (60 s) | App entrega agregarReporte al formulario. El hijo llama esa función con los datos y App actualiza el array. Las props también llevan datos hacia la lista. | App.jsx y FormularioReporte.jsx. |
| 7. Lista de reportes (45 s) | map convierte cada objeto en un componente Reporte. key usa el id. Si no hay datos o resultados, se muestra un mensaje distinto. | ListaReportes.jsx y Reporte.jsx. |
| 8. Eventos (50 s) | onClick ejecuta cambiarEstado o eliminarReporte. map cambia un reporte; filter quita el eliminado o selecciona los visibles. El filtro no borra datos. | App.jsx, Reporte.jsx y FiltroReportes.jsx. |
| 9. localStorage y useEffect (60 s) | JSON.stringify convierte a texto; JSON.parse recupera objetos. La lectura inicial ocurre antes del primer guardado; useEffect guarda al cambiar reportes. | recuperarReportes y useEffect en App.jsx. |
| 10. Demostración (90 s) | Crear los tres ejemplos, marcar uno atendido, eliminar otro, usar ambos filtros y recargar. Mostrar estadísticas y un formulario incompleto. | Navegador; seguir tabla de pruebas del README. |
| 11. Conclusión (25 s) | Aprendimos componentes, estado, props, eventos y persistencia local. El prototipo solo guarda datos en este navegador; una solución real necesitaría otros servicios fuera del alcance del curso. | Aplicación y pie académico. |

## Frases que pueden usar

- “Antes manipulábamos el DOM directamente. Ahora cambiamos el estado y React actualiza la pantalla”.
- “App conserva la lista; los hijos reciben datos y funciones mediante props”.
- “Las estadísticas se calculan, no se guardan por separado”.
- “useEffect sincroniza el array con el almacenamiento del navegador”.

## Preparación

1. Ejecutar npm install si es otro equipo y luego npm run dev.
2. Usar siempre la misma dirección y puerto para conservar los datos.
3. Tener abiertos App.jsx y los seis componentes.
4. Usar únicamente reportes de ejemplo. Eliminarlos al terminar si se desea empezar vacío.
5. No atribuir el sistema a la UNAC, municipalidad ni gobierno regional.
6. Explicar el código con palabras propias, sin leer cada línea.

## Preguntas previsibles

**¿Por qué no usamos fetch?** No hay API ni backend; localStorage cubre la persistencia del prototipo.

**¿Qué pasa al recargar?** El inicializador de useState lee los reportes guardados. El filtro vuelve a Todos.

**¿Por qué copiar con ...?** Para producir un array u objeto nuevo y actualizar el estado sin modificarlo directamente.

**¿Qué diferencia hay entre props y estado?** El estado pertenece al componente; las props llegan desde su padre.

**¿Por qué Date.now()?** Da un identificador numérico sencillo para este formulario manual; no pretende resolver identificadores de un sistema distribuido.

**¿Atendido significa que una autoridad intervino?** No: es un estado que el usuario del prototipo marca manualmente.
