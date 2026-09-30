import { useState } from 'react';

function FormularioReporte({ agregarReporte }) {
  const [distrito, setDistrito] = useState('');
  const [ubicacion, setUbicacion] = useState('');
  const [tipo, setTipo] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [mensaje, setMensaje] = useState('');

  function enviarReporte(event) {
    event.preventDefault();
    if (!distrito || !ubicacion.trim() || !tipo || !descripcion.trim()) {
      setMensaje('Completa todos los campos. No se aceptan solo espacios.');
      return;
    }
    // La función recibida por props entrega el reporte a App.
    agregarReporte({
      id: Date.now(), distrito, ubicacion: ubicacion.trim(), tipo,
      descripcion: descripcion.trim(), estado: 'Pendiente',
    });
    setDistrito('');
    setUbicacion('');
    setTipo('');
    setDescripcion('');
    setMensaje('Reporte registrado. Puedes consultarlo en el filtro Todos o Pendientes.');
  }

  return (
    <section className="panel formulario" aria-labelledby="titulo-formulario">
      <p className="etiqueta">PARTICIPA</p>
      <h2 id="titulo-formulario">Registrar nuevo reporte</h2>
      <p className="ayuda">Todos los campos son obligatorios.</p>
      <form onSubmit={enviarReporte}>
        <label htmlFor="distrito">Distrito</label>
        <select id="distrito" value={distrito} onChange={(event) => setDistrito(event.target.value)} required>
          <option value="">Selecciona un distrito</option>
          <option>Callao</option><option>Bellavista</option>
          <option>Carmen de la Legua-Reynoso</option><option>La Perla</option>
          <option>La Punta</option><option>Mi Perú</option><option>Ventanilla</option>
        </select>
        <label htmlFor="ubicacion">Ubicación referencial</label>
        <input id="ubicacion" value={ubicacion} onChange={(event) => setUbicacion(event.target.value)}
          placeholder="Ej. Cerca al parque principal" maxLength={160} required />
        <label htmlFor="tipo">Tipo de residuo</label>
        <select id="tipo" value={tipo} onChange={(event) => setTipo(event.target.value)} required>
          <option value="">Selecciona un tipo</option><option>Residuos domésticos</option>
          <option>Plásticos</option><option>Cartón y papel</option><option>Escombros</option>
          <option>Residuos orgánicos</option><option>Otros</option>
        </select>
        <label htmlFor="descripcion">Descripción</label>
        <textarea id="descripcion" value={descripcion} onChange={(event) => setDescripcion(event.target.value)}
          placeholder="Describe los residuos que observaste…" rows={4} maxLength={600} required />
        <p className="ayuda">El reporte se registrará como pendiente.</p>
        <button className="boton-principal" type="submit">Registrar reporte <span aria-hidden="true">＋</span></button>
        <p className="mensaje" role="status">{mensaje}</p>
      </form>
    </section>
  );
}
export default FormularioReporte;
