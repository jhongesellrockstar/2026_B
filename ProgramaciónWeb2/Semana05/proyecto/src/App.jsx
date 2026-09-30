import { useEffect, useState } from 'react';
import Header from './components/Header';
import Estadisticas from './components/Estadisticas';
import ResumenEstadistico from './components/ResumenEstadistico';
import FormularioReporte from './components/FormularioReporte';
import FiltroReportes from './components/FiltroReportes';
import ListaReportes from './components/ListaReportes';
import './App.css';

const claveReportes = 'callao-limpio-reportes';

function recuperarReportes() {
  // Lee antes del primer renderizado para no sobrescribir los datos guardados.
  try {
    const datos = JSON.parse(localStorage.getItem(claveReportes) || '[]');
    if (!Array.isArray(datos)) return [];
    return datos.filter((reporte) =>
      reporte && typeof reporte.id === 'number' &&
      typeof reporte.distrito === 'string' && typeof reporte.ubicacion === 'string' &&
      typeof reporte.tipo === 'string' && typeof reporte.descripcion === 'string' &&
      (reporte.estado === 'Pendiente' || reporte.estado === 'Atendido')
    );
  } catch {
    return [];
  }
}

function App() {
  const [reportes, setReportes] = useState(recuperarReportes);
  const [filtro, setFiltro] = useState('Todos');
  const [errorGuardado, setErrorGuardado] = useState('');

  // Guarda los reportes cada vez que cambia el array.
  useEffect(() => {
    try {
      localStorage.setItem(claveReportes, JSON.stringify(reportes));
      // oxlint-disable-next-line react/set-state-in-effect -- Refleja el resultado del almacenamiento externo.
      setErrorGuardado('');
    } catch {
      // oxlint-disable-next-line react/set-state-in-effect -- Informa si el navegador rechaza el guardado.
      setErrorGuardado('No se pudo guardar en este navegador. Los cambios se perderán al recargar.');
    }
  }, [reportes]);

  function agregarReporte(reporte) {
    setReportes([...reportes, reporte]);
  }

  function eliminarReporte(id) {
    setReportes(reportes.filter((reporte) => reporte.id !== id));
  }

  function cambiarEstado(id) {
    // map crea un array nuevo y cambia solamente el reporte elegido.
    setReportes(reportes.map((reporte) => {
      if (reporte.id === id) {
        return { ...reporte, estado: reporte.estado === 'Pendiente' ? 'Atendido' : 'Pendiente' };
      }
      return reporte;
    }));
  }

  const reportesFiltrados = reportes.filter((reporte) =>
    filtro === 'Todos' || reporte.estado === filtro
  );

  return (
    <>
      <Header />
      <main className="contenedor">
        <Estadisticas reportes={reportes} />
        <ResumenEstadistico reportes={reportes} />
        {errorGuardado && <p className="error" role="alert">{errorGuardado}</p>}
        <div className="contenido">
          <FormularioReporte agregarReporte={agregarReporte} />
          <section className="panel registros" aria-labelledby="titulo-reportes">
            <div className="titulo-seccion">
              <div><p className="etiqueta">SEGUIMIENTO</p><h2 id="titulo-reportes">Reportes ciudadanos</h2></div>
              <span className="cantidad">{reportesFiltrados.length} visibles</span>
            </div>
            <FiltroReportes filtro={filtro} setFiltro={setFiltro} />
            <ListaReportes reportes={reportesFiltrados} totalReportes={reportes.length}
              eliminarReporte={eliminarReporte} cambiarEstado={cambiarEstado} />
          </section>
        </div>
        <footer>Prototipo académico · Ingeniería de Sistemas · Programación Web 2
          <br />Los reportes se conservan en este navegador. No se envían a ninguna autoridad.
        </footer>
      </main>
    </>
  );
}
export default App;
