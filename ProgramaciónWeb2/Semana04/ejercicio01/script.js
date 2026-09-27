$(document).ready(function() {
    $('#procesar').click(function() {
        var monto = parseFloat($('#monto').val());
        var cuotas = parseInt($('#cuotas').val());

        if (isNaN(monto) || isNaN(cuotas)) {
            alert('Por favor, ingrese valores numéricos válidos.');
            return;
        }

        var montoMensual = monto / cuotas;
        $('#resultado').html('<corvus_file path="simulador_mensual.html">Monto a Pagar Mensual: ' + montoMensual.toFixed(2) + '</corvus_file>');
    });
});