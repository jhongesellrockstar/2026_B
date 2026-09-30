function Estadisticas({ reportes }) {
  // Se calculan desde el array, sin guardar otro estado.
  const pendientes = reportes.filter((reporte) => reporte.estado === 'Pendiente').length;
  const atendidos = reportes.filter((reporte) => reporte.estado === 'Atendido').length;
  return (
    <section className="estadisticas" aria-label="Estadísticas de reportes" aria-live="polite">
      <div className="estadistica"><span>Total de reportes</span><strong>{reportes.length}</strong><small>Puntos registrados</small></div>
      <div className="estadistica pendiente"><span>Pendientes</span><strong>{pendientes}</strong><small>Por atender</small></div>
      <div className="estadistica atendido"><span>Atendidos</span><strong>{atendidos}</strong><small>Atención registrada</small></div>
    </section>
  );
}
export default Estadisticas;
