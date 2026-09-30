# Práctica de reconstrucción — Callao Limpio

Cinco módulos del mismo proyecto. No crear cinco aplicaciones, instalar paquetes ni agregar componentes. Los fragmentos son ejercicios de estudio: no sustituyen los archivos completos de la versión final.

## Método de ensayo

1. Leer el objetivo y cerrar temporalmente la referencia.
2. Escribir el fragmento en un borrador del editor sin guardarlo en el proyecto. Compararlo con el archivo final y explicar cada decisión.
3. Para practicar el tutorial en ejecución, partir del proyecto sin cambios funcionales pendientes; sustituir temporalmente solo el bloque que se ensaya, reconstruirlo en su ubicación original y comprobarlo.
4. No borrar archivos completos ni dejar importaciones incompletas. Restaurar el bloque original al terminar. Revisar git diff antes de grabar; no descartar cambios ajenos.
5. Verificar con la interfaz y ejecutar npm run lint y npm run build tras el ensayo integrado.

Los fragmentos de JSX van dentro del return indicado; las declaraciones y funciones van antes del return, dentro del componente. No pegar varios return ni duplicar estados. La grabación puede comenzar con el proyecto funcional y reconstruir bloques seleccionados; no exige crear toda la aplicación desde cero.

## Módulo 1 — José

**JOSÉ ALEJANDRO ANCALLA ALARCON**

**Objetivo:** construir un componente sencillo y explicar cómo llega al navegador.

**Archivos:** src/components/Header.jsx y src/main.jsx; consultar index.html y src/App.jsx.

**Reconstrucción:** escribir en un borrador esta versión reducida de Header. En el ensayo con Vite, usar el archivo existente y restaurar después sus textos y clases finales.

```jsx
function Header() {
  return (
    <header>
      <h1>CALLAO LIMPIO</h1>
      <p>Registro ciudadano de puntos con acumulación de residuos</p>
    </header>
  );
}
export default Header;
```

Ubicar sin reescribir todo main.jsx:

```jsx
import App from './App.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

Este segundo fragmento requiere los imports de createRoot y StrictMode que ya existen en main.jsx. App importa Header y lo usa mediante <Header />. root es un elemento HTML, no un componente.

**Resultado esperado:** el título y subtítulo aparecen porque App incluye Header y main monta App.

**Prueba sencilla:** cambiar una palabra del título durante el ensayo, guardar y verla en el navegador. Restaurar el texto. Explicar por qué Vite refleja el cambio y qué responsabilidad tiene React.

**Autoevaluación:** seguir index.html → main.jsx → App → Header sin saltarse root.

## Módulo 2 — Diego

**DIEGO ENRIQUE CISNEROS AGURTO**

**Objetivo:** controlar un input y explicar cómo se envía un reporte válido.

**Archivo:** src/components/FormularioReporte.jsx.

**Reconstrucción A:** importar useState y declarar el estado en el componente existente.

```jsx
import { useState } from 'react';
```

```jsx
const [ubicacion, setUbicacion] = useState('');
```

Dentro del formulario:

```jsx
<label htmlFor="ubicacion">Ubicación referencial</label>
<input
  id="ubicacion"
  value={ubicacion}
  onChange={(event) => setUbicacion(event.target.value)}
  required
/>
```

**Reconstrucción B:** escribir el núcleo del manejador con los demás estados y agregarReporte ya declarados en el componente.

```jsx
function enviarReporte(event) {
  event.preventDefault();
  if (!distrito || !ubicacion.trim() || !tipo || !descripcion.trim()) {
    setMensaje('Completa todos los campos. No se aceptan solo espacios.');
    return;
  }
  agregarReporte({
    id: Date.now(),
    distrito,
    ubicacion: ubicacion.trim(),
    tipo,
    descripcion: descripcion.trim(),
    estado: 'Pendiente',
  });
  setDistrito('');
  setUbicacion('');
  setTipo('');
  setDescripcion('');
  setMensaje('Reporte registrado. Puedes consultarlo en el filtro Todos o Pendientes.');
}
```

Conectar con el onSubmit del form existente. No reconstruir los siete distritos de memoria: concentrarse en el patrón value/onChange.

**Resultado esperado:** escribir actualiza el estado; enviar datos válidos crea un reporte Pendiente y limpia los campos.

**Prueba sencilla:** completar selects, poner solo espacios en ubicación y descripción y enviar: aparece validación y no aumenta el total. Corregir los textos, enviar y comprobar una tarjeta nueva. Un campo completamente vacío puede ser detenido antes por required.

**Autoevaluación:** explicar por qué agregarReporte llega por props y por qué este componente no escribe en localStorage.

## Módulo 3 — Rodrigo

**RODRIGO ALONSO BRINGAS MARTINEZ**

**Objetivo:** transformar datos en tarjetas y entregar acciones sin ejecutarlas anticipadamente.

**Archivos:** src/components/ListaReportes.jsx y src/components/Reporte.jsx.

**Reconstrucción A:** conservar el import de Reporte, las props y el bloque de lista vacía. Reconstruir dentro del return:

```jsx
<div className="lista-reportes">
  {reportes.map((reporte) => (
    <Reporte
      key={reporte.id}
      reporte={reporte}
      eliminarReporte={eliminarReporte}
      cambiarEstado={cambiarEstado}
    />
  ))}
</div>
```

**Reconstrucción B:** dentro de Reporte, que ya recibe reporte y las funciones:

```jsx
<h3>{reporte.distrito}</h3>
<p>{reporte.descripcion}</p>
<button type="button" onClick={() => cambiarEstado(reporte.id)}>
  {reporte.estado === 'Atendido' ? 'Volver a pendiente' : 'Marcar atendido'}
</button>
```

El ternario elige un texto según una condición. En el archivo final se utiliza la variable atendido para expresar esa misma condición. Estudiar también el mensaje diferente cuando totalReportes es cero o solo el filtro está vacío.

**Resultado esperado:** una tarjeta por objeto; cada botón actúa sobre el id correspondiente.

**Prueba sencilla:** registrar dos ejemplos con ubicaciones diferentes desde la interfaz; cambiar el estado de uno y comprobar que el otro no cambia. No usar el índice del map como sustituto del id.

**Autoevaluación:** distinguir reporte (objeto), cambiarEstado (función) y key (identificador especial para React).

## Módulo 4 — Jesús

**JESÚS THENEE SOTO SALDARRIAGA**

**Objetivo:** actualizar el array principal y explicar su persistencia y su vista filtrada.

**Archivos:** src/App.jsx y src/components/FiltroReportes.jsx.

**Reconstrucción A:** dentro de App, conservando su estado existente:

```jsx
function eliminarReporte(id) {
  setReportes(reportes.filter((reporte) => reporte.id !== id));
}
```

**Reconstrucción B:** derivar los visibles a partir de reportes y filtro:

```jsx
const reportesFiltrados = reportes.filter((reporte) =>
  filtro === 'Todos' || reporte.estado === filtro
);
```

Relacionar con un botón existente de FiltroReportes:

```jsx
<button type="button" onClick={() => setFiltro('Pendiente')}>
  Pendientes
</button>
```

El fragmento del botón omite el atributo aria-pressed para centrarse en el evento; conservar ese atributo en la versión final.

**Lectura guiada del guardado:** este fragmento mínimo es únicamente conceptual para escribir en el borrador. El código final conserva try/catch y el aviso de error, que no deben eliminarse.

```jsx
useEffect(() => {
  localStorage.setItem(claveReportes, JSON.stringify(reportes));
}, [reportes]);
```

Explicar además la declaración real:

```jsx
const [reportes, setReportes] = useState(recuperarReportes);
```

recuperarReportes lee y convierte JSON antes del primer guardado. Estudiar su validación y el retorno [] ante datos inválidos. El efecto sincroniza después del renderizado. No agregar un segundo efecto de lectura que permita sobrescribir accidentalmente los datos iniciales.

**Resultado esperado:** eliminar cambia el array; filtrar cambia solamente los visibles; recargar restaura los reportes y reinicia el filtro a Todos.

**Prueba sencilla:** con un ejemplo temporal presente, anotar total, eliminarlo y comprobar total anterior menos uno; filtrar Pendientes/Atendidos y recargar en la misma dirección. Conservar los demás ejemplos.

**Autoevaluación:** explicar diferencia entre filter usado para eliminar y filter usado para visualizar. Mostrar qué guarda stringify y qué recupera parse.

## Módulo 5 — Jhon

**JHON GESELL VILLANUEVA PORTELLA**

**Objetivo:** derivar indicadores y convertir números en estilos sin guardar otro estado.

**Archivos:** src/components/Estadisticas.jsx, src/components/ResumenEstadistico.jsx y src/App.css; consultar props en App.jsx.

**Reconstrucción A:** dentro de ResumenEstadistico, que recibe reportes:

```jsx
const total = reportes.length;
const pendientes = reportes.filter((reporte) => reporte.estado === 'Pendiente').length;
const atendidos = reportes.filter((reporte) => reporte.estado === 'Atendido').length;
let porcentajePendientes = 0;
let porcentajeAtendidos = 0;
if (total > 0) {
  porcentajePendientes = pendientes / total * 100;
  porcentajeAtendidos = atendidos / total * 100;
}
```

**Reconstrucción B:** contar distritos con un for y un objeto local; no mutar el array reportes.

```jsx
const cantidadesPorDistrito = {};
let mayorCantidad = 0;
for (let i = 0; i < reportes.length; i++) {
  const distrito = reportes[i].distrito;
  if (!cantidadesPorDistrito[distrito]) {
    cantidadesPorDistrito[distrito] = 0;
  }
  cantidadesPorDistrito[distrito]++;
  mayorCantidad = Math.max(mayorCantidad, cantidadesPorDistrito[distrito]);
}
const distritos = Object.keys(cantidadesPorDistrito);
```

Dentro del map de distritos que ya existe en el JSX:

```jsx
const cantidad = cantidadesPorDistrito[distrito];
const ancho = cantidad / mayorCantidad * 100;
```

Usar ancho en la barra interior:

```jsx
<div className="barra-distrito" style={{ width: `${ancho}%` }} />
```

Mostrar, sin reconstruir todo el diseño, que el círculo recibe fondoCircular mediante style y que conic-gradient cambia de color en porcentajePendientes. Si no hay datos, el fondo es neutro y no se recorre ninguna barra. La leyenda redondea a un decimal; el gradiente utiliza el porcentaje calculado.

**Resultado esperado:** con 8 reportes, 5 pendientes y 3 atendidos, círculo 62,5 %/37,5 %. Con distritos 3/2/2/1, barras 100 %/66,7 %/66,7 %/33,3 % respecto al máximo.

**Prueba sencilla:** cambiar un reporte pendiente a atendido: el total y las barras quedan iguales, pero pasan a 4 pendientes y 4 atendidos, es decir 50 %/50 %. Volverlo a pendiente. Registrar o eliminar un ejemplo cambia total y conteo por distrito. Filtrar no altera los gráficos.

**Autoevaluación:** justificar por qué el porcentaje del círculo y el ancho de barra usan denominadores diferentes.

## Ensayo integrado y restauración

Seguir el orden José → Diego → Rodrigo → Jesús → Jhon. Practicar ocho minutos por persona, incluyendo escritura y transición, y cronometrar los 40 minutos. Jhon reserva tres minutos para la demostración completa descrita en TUTORIAL_GRUPAL.md.

Usar reportes académicos introducidos desde el formulario. Para la demostración preparada, tener Callao 3, Bellavista 2, Ventanilla 2 y La Perla 1; marcar tres atendidos. No incorporar esos datos a App.jsx. Eliminar únicamente los ejemplos temporales creados durante el ensayo.

Antes de entregar: verificar que todos los bloques reconstruidos coinciden con la versión final, que no queden borradores guardados en src y que git diff no muestre cambios funcionales accidentales. No hacer push hasta revisar los documentos.

