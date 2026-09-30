function ResumenEstadistico({ reportes }) {
  const total = reportes.length;
  const pendientes = reportes.filter((reporte) => reporte.estado === 'Pendiente').length;
  const atendidos = reportes.filter((reporte) => reporte.estado === 'Atendido').length;
  let porcentajePendientes = 0;
  let porcentajeAtendidos = 0;

  // Evita dividir entre cero cuando todavía no hay reportes.
  if (total > 0) {
    porcentajePendientes = pendientes / total * 100;
    porcentajeAtendidos = atendidos / total * 100;
  }

  const cantidadesPorDistrito = {};
  let mayorCantidad = 0;
  // Cuenta cada distrito y conserva la cantidad más alta para escalar las barras.
  for (let i = 0; i < reportes.length; i++) {
    const distrito = reportes[i].distrito;
    if (!cantidadesPorDistrito[distrito]) {
      cantidadesPorDistrito[distrito] = 0;
    }
    cantidadesPorDistrito[distrito]++;
    mayorCantidad = Math.max(mayorCantidad, cantidadesPorDistrito[distrito]);
  }
  const distritos = Object.keys(cantidadesPorDistrito);

  let fondoCircular = '#e4e9e2';
  if (total > 0) {
    fondoCircular = `conic-gradient(#c0923d 0% ${porcentajePendientes}%, #6c9b67 ${porcentajePendientes}% 100%)`;
  }

  return (
    <section className="panel resumen-estadistico" aria-labelledby="titulo-resumen">
      <p className="etiqueta">PANORAMA GENERAL</p>
      <h2 id="titulo-resumen">Resumen estadístico</h2>
      <p className="ayuda">Incluye todos los reportes, independientemente del filtro seleccionado.</p>
      <div className="graficos-resumen">
        <div>
          <h3>Estado de los reportes</h3>
          <div className="resumen-estados">
            <div className="grafico-circular" style={{ background: fondoCircular }} aria-hidden="true" />
            <div className="leyenda-estados">
              <p><span className="muestra-color color-pendiente" aria-hidden="true" />Pendientes: <strong>{pendientes}</strong> ({Math.round(porcentajePendientes * 10) / 10} %)</p>
              <p><span className="muestra-color color-atendido" aria-hidden="true" />Atendidos: <strong>{atendidos}</strong> ({Math.round(porcentajeAtendidos * 10) / 10} %)</p>
              {total === 0 && <p className="ayuda">Aún no hay datos para representar.</p>}
            </div>
          </div>
        </div>
        <div>
          <h3>Reportes por distrito</h3>
          {total === 0 ? <p className="ayuda">Aún no hay datos para representar.</p> : (
            <ul className="barras-distritos">
              {distritos.map((distrito) => {
                const cantidad = cantidadesPorDistrito[distrito];
                const ancho = cantidad / mayorCantidad * 100;
                return (
                  <li key={distrito}>
                    <div className="etiqueta-barra"><span>{distrito}</span><strong>{cantidad}</strong></div>
                    <div className="fondo-barra" aria-hidden="true">
                      <div className="barra-distrito" style={{ width: `${ancho}%` }} />
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      </div>
    </section>
  );
}

export default ResumenEstadistico;
