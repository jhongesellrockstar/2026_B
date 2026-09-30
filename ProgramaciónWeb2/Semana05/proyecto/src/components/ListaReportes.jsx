import Reporte from './Reporte';

function ListaReportes({ reportes, totalReportes, eliminarReporte, cambiarEstado }) {
  if (reportes.length === 0) {
    return (
      <div className="vacio">
        <span className="simbolo-vacio" aria-hidden="true">♧</span>
        <h3>{totalReportes === 0 ? 'No existen reportes registrados.' : 'No existen reportes con este filtro.'}</h3>
        <p>{totalReportes === 0 ? 'Completa el formulario para registrar el primer punto.' : 'Selecciona otro estado para consultar tus reportes.'}</p>
      </div>
    );
  }
  return (
    <div className="lista-reportes">
      {reportes.map((reporte) => (
        <Reporte key={reporte.id} reporte={reporte}
          eliminarReporte={eliminarReporte} cambiarEstado={cambiarEstado} />
      ))}
    </div>
  );
}
export default ListaReportes;
