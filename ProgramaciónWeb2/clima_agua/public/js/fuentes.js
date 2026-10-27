// AJAX sencillo: evento -> fetch -> Controller -> Model -> MySQL -> HTML parcial.
const buscador = document.getElementById('buscador');
if (buscador) {
    const resultados = document.getElementById('resultados');
    const estado = document.getElementById('estado-busqueda');
    let temporizador;
    let solicitud;

    async function buscar(pagina = 1) {
        clearTimeout(temporizador);
        if (solicitud) solicitud.abort();
        solicitud = new AbortController();
        const parametros = new URLSearchParams(new FormData(buscador));
        parametros.set('page', pagina);
        estado.textContent = 'Buscando fuentes…';
        resultados.setAttribute('aria-busy', 'true');
        try {
            const respuesta = await fetch(buscador.dataset.ajax + '?' + parametros, {
                signal: solicitud.signal, headers: {'X-Requested-With': 'XMLHttpRequest'}
            });
            if (!respuesta.ok) throw new Error('Error en la búsqueda');
            const html = await respuesta.text();
            resultados.innerHTML = html;
            // Conserva una URL normal para recargar o compartir localmente la búsqueda.
            history.replaceState(null, '', buscador.action + '?' + parametros);
            estado.textContent = 'Resultados actualizados con AJAX, sin recargar la página.';
            resultados.removeAttribute('aria-busy');
        } catch (error) {
            if (error.name !== 'AbortError') {
                estado.textContent = 'No se pudo actualizar. Pulsa Buscar para intentar de nuevo.';
                resultados.removeAttribute('aria-busy');
            }
        }
    }
    buscador.q.addEventListener('input', function () {
        clearTimeout(temporizador);
        // Cancela la búsqueda anterior para que no muestre resultados antiguos.
        if (solicitud) solicitud.abort();
        temporizador = setTimeout(function () { buscar(); }, 300);
    });
    buscador.addEventListener('change', function (evento) {
        if (evento.target.tagName === 'SELECT') buscar();
    });
    // El botón Buscar hace una búsqueda GET normal; funciona incluso sin JavaScript.
    resultados.addEventListener('click', function (evento) {
        const enlace = evento.target.closest('.paginacion a');
        if (!enlace || evento.ctrlKey || evento.metaKey || evento.shiftKey) return;
        evento.preventDefault();
        buscar(new URL(enlace.href).searchParams.get('page') || 1);
    });
}
// Delegación: también funciona en las filas recibidas por AJAX.
document.addEventListener('submit', function (evento) {
    if (evento.target.matches('form.eliminar') && !confirm('¿Está seguro de eliminar esta fuente?')) {
        evento.preventDefault();
    }
});
