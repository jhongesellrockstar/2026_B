function FiltroReportes({ filtro, setFiltro }) {
  return (
    <div className="filtros" role="group" aria-label="Filtrar por estado">
      <button type="button" aria-pressed={filtro === 'Todos'} onClick={() => setFiltro('Todos')}>Todos</button>
      <button type="button" aria-pressed={filtro === 'Pendiente'} onClick={() => setFiltro('Pendiente')}>Pendientes</button>
      <button type="button" aria-pressed={filtro === 'Atendido'} onClick={() => setFiltro('Atendido')}>Atendidos</button>
    </div>
  );
}
export default FiltroReportes;
