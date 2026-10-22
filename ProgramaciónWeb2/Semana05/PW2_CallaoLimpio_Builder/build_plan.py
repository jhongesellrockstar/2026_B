"""Plan declarativo. La referencia se lee; nunca se modifica."""
from dataclasses import dataclass
from pathlib import Path

REFERENCE = Path(r'C:\Users\ACER\Documents\GitHub\2026_B\ProgramaciónWeb2\Semana05\proyecto')
TARGET = REFERENCE.parent / 'proyecto_tutorial'
FILES = ('src/main.jsx', 'src/index.css', 'src/App.jsx', 'src/App.css',
         'src/components/Header.jsx', 'src/components/FormularioReporte.jsx',
         'src/components/ListaReportes.jsx', 'src/components/Reporte.jsx',
         'src/components/FiltroReportes.jsx', 'src/components/Estadisticas.jsx',
         'src/components/ResumenEstadistico.jsx')
AUXILIARIES = ('package.json', 'package-lock.json', 'vite.config.js', 'index.html', '.oxlintrc.json')
SPEEDS = (0.005, 0.010, 0.015, 0.020, 0.030, 0.040)


@dataclass(frozen=True)
class Step:
    numero: int
    integrante: str
    archivo: str
    descripcion: str
    modo: str
    contenido: str
    guardar: bool = True
    accion: str = 'EDIT'
    reemplazar: bool = False
    # For an insertion at a specific offset; None means append.
    offset: int | None = None


def source_bytes(reference=REFERENCE):
    return {p: (reference / p).read_bytes() for p in FILES}


def make_plan(reference=REFERENCE):
    texts = {p: b.decode('utf-8-sig').replace('\r\n', '\n')
             for p, b in source_bytes(reference).items()}
    steps = []

    def add(who, file, desc, mode='INSERT', text='', action='EDIT', replace=False, offset=None):
        if action != 'EDIT':
            mode = 'COMMAND' if action in ('VITE', 'AUX', 'INSTALL', 'DIRS', 'BUILD', 'DEV') else action
        steps.append(Step(len(steps) + 1, who, file, desc, mode, text,
                          True, action, replace, offset))

    def parts(who, file, markers, labels, modes=None, text=None):
        content = texts[file] if text is None else text
        positions = [0]
        for marker in markers:
            pos = content.find(marker, positions[-1] + 1)
            if pos < 0:
                raise ValueError(f'La referencia cambió: falta {marker!r} en {file}')
            positions.append(pos)
        positions.append(len(content))
        if len(labels) != len(positions) - 1:
            raise ValueError('Número de etiquetas incorrecto')
        modes = modes or ['TYPE'] * len(labels)
        for i, label in enumerate(labels):
            add(who, file, label, modes[i], content[positions[i]:positions[i+1]], replace=i == 0)

    add('José', '', 'Crear carpeta vacía y abrir SOLO el destino en VS Code', action='START')
    add('José', '', 'Generar proyecto React con Vite (comando real)',
        text='npm create vite@latest . -- --template react --no-interactive --no-immediate', action='VITE')
    add('José', '', 'Ajustar auxiliares generados a la referencia, sin copiar src', action='AUX')
    add('José', '', 'Instalar dependencias (npm install)', text='npm install', action='INSTALL')
    add('José', 'src/components', 'Limpiar plantilla inicial de Vite y preparar components (terminal visible)', action='DIRS')
    parts('José', 'src/main.jsx', ['createRoot('], ['Imports de entrada', 'Montaje de App en root'])
    add('José', 'src/index.css', 'Estilos globales: explicar box-sizing, controles y foco',
        text=texts['src/index.css'], replace=True)
    parts('José', 'src/components/Header.jsx', ['  return (', 'export default'],
          ['Declaración de Header', 'JSX completo de cabecera', 'Exportación de Header'])
    add('José', 'src/App.jsx', 'App mínima: solo Header; sin imports futuros', 'TYPE',
        "import Header from './components/Header';\n\nfunction App() {\n  return <Header />;\n}\n\nexport default App;\n", replace=True)

    parts('Diego', 'src/components/FormularioReporte.jsx',
          ['function FormularioReporte', '  const [distrito', '  function enviarReporte',
           '    // La función', '    setDistrito', '  return (',
           '          <option value="">Selecciona un distrito', '        </select>',
           '          <option value="">Selecciona un tipo', '        </select>\n        <label htmlFor="descripcion"'],
          ['Importar useState', 'Componente y prop agregarReporte', 'Cinco estados del formulario',
           'Evento y validación con trim', 'Objeto del reporte y llamada al padre',
           'Limpiar campos y mensaje final', 'Sección, formulario y select controlado',
           'Opciones de distrito: explicar datos estáticos', 'Ubicación y select de tipo',
           'Opciones de residuo: explicar datos estáticos', 'Textarea, botón, mensaje y export'],
          ['TYPE']*6 + ['INSERT', 'INSERT', 'TYPE', 'INSERT', 'INSERT'])

    parts('Rodrigo', 'src/components/ListaReportes.jsx',
          ['function ListaReportes', '  if (reportes.length', '  return (\n    <div className="lista-reportes">'],
          ['Import de Reporte (aún no se monta)', 'Props de ListaReportes',
           'Dos casos vacíos y renderizado condicional', 'map, key y props al hijo'])
    parts('Rodrigo', 'src/components/Reporte.jsx', ['  return (', '      <div className="acciones">'],
          ['Props y condición atendido', 'Datos de la tarjeta', 'Callbacks, ternario y botones'])
    css = texts['src/App.css']
    start, end = css.index('.resumen-estadistico'), css.index('.cabecera {')
    base, graph = css[:start] + css[end:], css[start:end]
    add('Rodrigo', 'src/App.css', 'CSS principal y responsive: explicar las clases JSX',
        text=base, replace=True)

    parts('Jesús', 'src/components/FiltroReportes.jsx', ['  return ('],
          ['Props del filtro', 'Tres botones y aria-pressed'])
    final_app = texts['src/App.jsx']
    temporary = final_app
    for name in ('Estadisticas', 'ResumenEstadistico'):
        temporary = temporary.replace('import '+name+' from', '// import '+name+' from')
        temporary = temporary.replace('<'+name+' reportes={reportes} />', '{/* <'+name+' reportes={reportes} /> */}')
    parts('Jesús', 'src/App.jsx',
          ['const claveReportes', 'function recuperarReportes', 'function App()',
           '  // Guarda los reportes', '  function agregarReporte', '  function eliminarReporte',
           '  function cambiarEstado', '  const reportesFiltrados', '  return (\n    <>'],
          ['Imports: estadísticas temporalmente comentadas', 'Clave de localStorage',
           'Lectura inicial, validación y recuperación segura', 'Estado de App',
           'Persistencia con useEffect y manejo de error', 'Agregar con spread',
           'Eliminar con filter', 'Cambiar estado con map', 'Filtrar visibles',
           'Conectar componentes: explicar props y dos llamadas comentadas'],
          ['TYPE']*9 + ['INSERT'], text=temporary)

    parts('Jhon', 'src/components/Estadisticas.jsx', ['  return ('],
          ['Conteos derivados del array', 'Tres indicadores y export'])
    parts('Jhon', 'src/components/ResumenEstadistico.jsx',
          ['  // Evita dividir', '  const cantidadesPorDistrito', '  for (',
           '  const distritos', '  let fondoCircular', '  return ('],
          ['Props, conteos y porcentajes iniciales', 'Evitar división entre cero',
           'Objeto de contadores por distrito', 'Recorrer y conservar el máximo',
           'Nombres de distritos con Object.keys', 'Fondo circular mediante conic-gradient',
           'JSX del resumen: explicar leyenda, map, ancho y style'],
          ['TYPE']*6 + ['INSERT'])
    add('Jhon', 'src/App.css', 'Insertar CSS de gráficos en su posición original; explicar reglas',
        text=graph, offset=start)
    add('Jhon', 'src/App.jsx', 'Integración: habilitar los dos imports y dos llamadas JSX',
        'TYPE', text=final_app, replace=True)
    add('Jhon', '', 'Guardar y verificar los 11 archivos; conservar bytes/EOL originales', action='VERIFY')
    add('FINAL', '', 'Compilar la aplicación construida (npm run build)', text='npm run build', action='BUILD')
    add('FINAL', '', 'Iniciar npm run dev en puerto libre y verificar respuesta HTTP', action='DEV')
    add('FINAL', '', 'Abrir Microsoft Edge y comenzar demostración de dos minutos', action='BROWSER')
    return steps


def verificar_resultado(target=TARGET, reference=REFERENCE):
    """Comparación estricta de bytes, sin modificar ningún archivo."""
    result = {}
    for p in FILES:
        dest = target / p
        result[p] = ('FALTA' if not dest.is_file() else
                     'OK' if dest.read_bytes() == (reference / p).read_bytes() else 'DIFERENTE')
    return result


def simulate(steps):
    """Reconstruye en memoria los pasos de edición; no ejecuta comandos."""
    state = {}
    for s in steps:
        if s.accion != 'EDIT':
            continue
        before = state.get(s.archivo, '')
        offset = len(before) if s.offset is None else s.offset
        state[s.archivo] = s.contenido if s.reemplazar else before[:offset] + s.contenido + before[offset:]
    return state
