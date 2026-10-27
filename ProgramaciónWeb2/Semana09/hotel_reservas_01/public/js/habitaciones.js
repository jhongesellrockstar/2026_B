const tipo = document.getElementById('tipo');
if (tipo) {
    const capacidades = { sencilla: 1, doble: 2, triple: 3 };
    const precios = { sencilla: 100, doble: 200, triple: 300 };
    function actualizarTarifa() {
        document.getElementById('capacidad').value = capacidades[tipo.value] || '';
        document.getElementById('precio_noche').value = precios[tipo.value] || '';
    }
    tipo.addEventListener('change', actualizarTarifa);
    actualizarTarifa();
}
