# Callao Limpio

## Descripción

Prototipo académico de Programación Web 2, elaborado para estudiantes de Ingeniería de Sistemas de la Universidad Nacional del Callao. Permite registrar y dar seguimiento a puntos con acumulación de residuos sólidos en el Callao.

No es una aplicación oficial de la universidad, municipalidades ni gobierno regional. Los reportes no se envían a autoridades: son datos locales para practicar React.

## Tecnologías utilizadas

- React: componentes e interfaz.
- Vite: desarrollo y compilación.
- JavaScript, HTML y CSS.
- localStorage: almacenamiento en el navegador.

Sin backend, APIs externas, autenticación ni bibliotecas de interfaz. Las herramientas de desarrollo incluidas por la plantilla Vite no forman parte de la lógica de la aplicación. Los paquetes @types de la plantilla ayudan al editor; el código del proyecto es JavaScript, no TypeScript.

## Requisitos

- Windows 11.
- Node.js 20 o superior **compatible con Vite**: 20.19+ en la rama 20, o 22.12+ en las ramas posteriores. Se recomienda usar el entorno probado.
- npm.
- Navegador moderno, por ejemplo Microsoft Edge.

Entorno comprobado: **Node.js v24.15.0 y npm 11.12.1**.

## Instalación en Windows 11

1. Descarga o copia la carpeta del proyecto.
2. Abre PowerShell.
3. Entra a la carpeta (ajusta la ruta):

   ~~~powershell
   cd "C:\ruta\donde\se\encuentre\proyecto"
   ~~~

   En el equipo original:

   ~~~powershell
   cd "C:\Users\ACER\Documents\GitHub\2026_B\ProgramaciónWeb2\Semana05\proyecto"
   ~~~

4. Comprueba las versiones:

   ~~~powershell
   node -v
   npm -v
   ~~~

5. Instala las dependencias:

   ~~~powershell
   npm install
   ~~~

6. Inicia la aplicación:

   ~~~powershell
   npm run dev
   ~~~

7. Abre en Microsoft Edge la dirección que muestra Vite, normalmente http://localhost:5173/. Si ese puerto está ocupado, utiliza el que indique la terminal.
8. Mantén PowerShell abierto. Para detener el servidor, pulsa Ctrl+C.

Si PowerShell bloquea npm.ps1, usa npm.cmd install y npm.cmd run dev, sin cambiar la política de seguridad de Windows.

### Compartir el proyecto

No necesitas compartir **node_modules** ni **dist**; están ignorados en .gitignore.
Conserva **package.json** y **package-lock.json**, junto con el código y la configuración.
Cada integrante reconstruye las dependencias con npm install.

### Compilar y revisar

~~~powershell
npm run build
npm run lint
npm run preview
~~~

build genera dist. preview permite revisar esa compilación en la dirección indicada por Vite. No abras index.html directamente con doble clic: utiliza el servidor de Vite.

## Uso

1. Completa distrito, ubicación referencial, tipo de residuo y descripción.
2. Pulsa **Registrar reporte**. Se crea como **Pendiente** y se limpia el formulario.
3. Consulta **Todos**, **Pendientes** o **Atendidos**. Si registras con otro filtro activo, cambia a Todos o Pendientes para ver el nuevo reporte.
4. Pulsa **Marcar atendido** o **Volver a pendiente**.
5. Pulsa **Eliminar** para quitar un reporte. La eliminación es inmediata.
6. Las estadísticas siempre cuentan todos los reportes, aunque el filtro muestre una parte.

Los siete distritos y seis tipos de residuo están definidos directamente en el formulario para facilitar su lectura.

## Estructura del proyecto


| Archivo | Responsabilidad |
| --- | --- |
| src/main.jsx | Monta App dentro de root y carga los estilos generales. |
| src/App.jsx | Mantiene reportes y filtro; agrega, elimina, cambia estado y guarda. |
| src/components/Header.jsx | Nombre, subtítulo y contexto académico. |
| src/components/Estadisticas.jsx | Calcula total, pendientes y atendidos. |
| src/components/ResumenEstadistico.jsx | Representa estados y cantidades por distrito con CSS. |
| src/components/FormularioReporte.jsx | Controla campos, valida y entrega el reporte a App. |
| src/components/FiltroReportes.jsx | Cambia el filtro mediante botones. |
| src/components/ListaReportes.jsx | Muestra mensajes vacíos o recorre reportes con map. |
| src/components/Reporte.jsx | Presenta un reporte y sus dos acciones. |
| src/App.css | Diseño de la aplicación y adaptación a pantallas pequeñas. |
| src/index.css | Estilos generales, tipografía y foco de teclado. |
| index.html | Documento HTML con idioma español y elemento root. |
| GUIA_VIDEO.md | Orden sugerido para la exposición. |

## Conceptos de React utilizados


- **Componentes:** funciones que devuelven una parte de la interfaz, como Header o Reporte.
- **JSX:** HTML escrito dentro de JavaScript. Las llaves insertan expresiones, por ejemplo reportes.length.
- **Props:** datos y funciones que un padre entrega a sus hijos. App pasa agregarReporte al formulario; ListaReportes pasa reporte a cada tarjeta.
- **useState:** conserva valores entre renderizados. App guarda el array; el formulario guarda cada campo. Cambiar el estado hace que React actualice la pantalla.
- **useEffect:** en App guarda el array en localStorage cuando cambia reportes. La dependencia [reportes] indica cuándo debe repetirse.
- **Eventos:** onSubmit ejecuta enviarReporte; preventDefault evita recargar. onChange actualiza campos; onClick cambia estados, filtros o elimina.
- **Listas:** map en ListaReportes genera una tarjeta por objeto. key usa el id para identificar cada elemento.
- **Renderizado condicional:** ListaReportes muestra mensajes cuando no hay resultados; Reporte cambia el texto del botón según el estado.
- **localStorage:** es una API del navegador, no una función de React. Conserva texto entre recargas.

En las semanas anteriores se modificaba el DOM con getElementById y createElement. Aquí se cambia el estado y React actualiza el DOM. No es necesario crear o eliminar nodos manualmente.

### Flujo de los datos

FormularioReporte → agregarReporte (prop) → estado en App → ListaReportes → Reporte.

El formulario construye un objeto con id (Date.now()), distrito, ubicacion, tipo, descripcion y estado. El operador ... copia el array al agregar o el objeto al cambiar su estado; filter crea un array sin el eliminado. No se modifica directamente el estado existente.

## Cómo se guardan los reportes

La clave utilizada es **callao-limpio-reportes**.

Al iniciar, useState(recuperarReportes) ejecuta la lectura con getItem y JSON.parse. Se pasa la función sin paréntesis para usarla como inicializador. Así, el primer guardado no reemplaza los reportes anteriores por un array vacío.

Después, useEffect usa setItem y JSON.stringify cada vez que cambia el array. No se guardan el filtro ni las estadísticas.

La lectura devuelve una lista vacía si el JSON no puede interpretarse; también descarta objetos incompletos. Si el navegador impide guardar, aparece un aviso. Los datos dependen del navegador y del origen (dirección y puerto): localhost y 127.0.0.1 tienen almacenamientos distintos. Borrar datos del navegador elimina los reportes. No existe sincronización entre equipos o pestañas abiertas.

## Pruebas funcionales para repetir

Empieza sin reportes o elimina únicamente tus datos de prueba.

| Paso | Acción | Resultado esperado |
| --- | --- | --- |
| 1 | Registrar Callao / Av. Argentina cerca al cruce principal / Residuos domésticos / Acumulación de bolsas y residuos cerca de la vía. | Una tarjeta pendiente; formulario limpio. |
| 2 | Agregar Bellavista / Cerca al parque principal / Plásticos / Botellas y bolsas plásticas acumuladas. | Total 2. |
| 3 | Agregar Ventanilla / Zona cercana al mercado / Residuos orgánicos / Residuos de alimentos acumulados en la vía pública. | Total 3, pendientes 3, atendidos 0. |
| 4 | Marcar Callao atendido. | Total 3, pendientes 2, atendidos 1. |
| 5 | Eliminar Bellavista. | Total 2, pendientes 1, atendidos 1. |
| 6 | Filtrar Pendientes y luego Atendidos. | Ventanilla y Callao, respectivamente. |
| 7 | Recargar en la misma dirección. | Se conservan ambos reportes y sus estados. |
| 8 | Revisar la consola con F12. | Sin errores durante el uso normal. |

Comprueba además campos vacíos, espacios en blanco, retorno a pendiente y mensajes de lista vacía. Reduce el ancho de la ventana: formulario y lista deben apilarse.

## Guía de exposición

Consulta GUIA_VIDEO.md. Explica especialmente cómo viajan los datos y por qué las estadísticas se calculan desde el array.

La exposición se organiza en cinco módulos del mismo proyecto: ocho minutos por integrante, aproximadamente 40 minutos en total. Consulta [TUTORIAL_GRUPAL.md](TUTORIAL_GRUPAL.md) para la distribución definitiva, el flujo y las preguntas; usa [PRACTICA_TUTORIAL.md](PRACTICA_TUTORIAL.md) para ensayar la reconstrucción de fragmentos sin modificar la versión funcional final.

## Resumen estadístico

Las visualizaciones se generan con React y CSS, sin bibliotecas de gráficos ni estados adicionales. ResumenEstadistico.jsx recibe todos los reportes por props y calcula los valores en cada renderizado.

El círculo usa conic-gradient: divide pendientes y atendidos entre el total y multiplica por 100. Sin reportes, muestra un círculo neutro. Las barras cuentan reportes por distrito mediante un for; su ancho es cantidad / mayorCantidad * 100. Solo aparecen distritos con reportes. Los porcentajes de la leyenda se redondean a un decimal.

Al registrar, eliminar o cambiar un estado, ambos gráficos se actualizan. Los filtros solo afectan la lista, no el resumen. Object.keys convierte las claves del objeto de cantidades en un array para recorrerlo con map.
