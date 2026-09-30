function Reporte({ reporte, eliminarReporte, cambiarEstado }) {
  const atendido = reporte.estado === 'Atendido';
  return (
    <article className="reporte">
      <div className="titulo-reporte">
        <h3>{reporte.distrito}</h3>
        <span className={atendido ? 'estado atendido' : 'estado pendiente'}>{reporte.estado}</span>
      </div>
      <p className="ubicacion">{reporte.ubicacion}</p>
      <p className="tipo-residuo">{reporte.tipo}</p>
      <p className="descripcion">{reporte.descripcion}</p>
      <div className="acciones">
        <button type="button" className="boton-estado" onClick={() => cambiarEstado(reporte.id)}>
          {atendido ? 'Volver a pendiente' : 'Marcar atendido'}
        </button>
        <button type="button" className="boton-eliminar" onClick={() => eliminarReporte(reporte.id)}>Eliminar</button>
      </div>
    </article>
  );
}
export default Reporte;
