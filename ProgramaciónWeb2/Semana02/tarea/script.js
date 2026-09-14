const formulario = document.getElementById("formulario");
const contenedor = document.getElementById("invitados");
const cantidad = document.getElementById("cantidad");
const estado = document.getElementById("estado");
let siguienteId = 1;

document.getElementById("agregar-invitados").addEventListener("click", agregarInvitados);
formulario.addEventListener("submit", function (event) {
    event.preventDefault();
    estado.textContent = "";
    if (validarFormulario()) {
        descargarArchivo(generarContenidoTxt());
        estado.textContent = "Se solicitó la descarga de invitados.txt. Revisa las descargas de Edge.";
    } else {
        estado.textContent = "Revisa los errores indicados junto a los campos.";
        formulario.querySelector('[aria-invalid="true"]').focus();
    }
});

function validarCantidad() {
    limpiarError(cantidad);
    const numero = Number(cantidad.value);
    if (cantidad.value === "" || !Number.isInteger(numero) || numero < 1 || numero > 50) {
        mostrarError(cantidad, "Ingrese una cantidad entera entre 1 y 50.");
        return false;
    }
    return true;
}

function agregarInvitados() {
    estado.textContent = "";
    if (!validarCantidad()) {
        return;
    }
    // Conserva los datos existentes y genera N bloques nuevos mediante el DOM.
    for (let i = 0; i < Number(cantidad.value); i++) {
        contenedor.appendChild(crearBloqueInvitado());
    }
    document.getElementById("error-invitados").textContent = "";
    renumerarInvitados();
}

function crearBloqueInvitado() {
    const bloque = document.createElement("article");
    bloque.className = "invitado";
    const cabecera = document.createElement("div");
    cabecera.className = "cabecera-invitado";
    const titulo = document.createElement("h3");
    const boton = document.createElement("button");
    boton.type = "button";
    boton.className = "eliminar";
    boton.textContent = "✕";
    boton.addEventListener("click", function () {
        eliminarInvitado(bloque);
    });
    cabecera.append(titulo, boton);
    bloque.appendChild(cabecera);
    // El identificador no se reutiliza aunque se eliminen o renumeren invitados.
    const id = siguienteId;
    siguienteId++;
    bloque.appendChild(crearCampo("Nombre completo", "nombre", "text", id));
    bloque.appendChild(crearCampo("Correo electrónico", "correo", "email", id));
    bloque.appendChild(crearCampo("Teléfono", "telefono", "tel", id));
    bloque.appendChild(crearCampo("Relación con el anfitrión", "relacion", "select", id));
    return bloque;
}

function crearCampo(texto, nombre, tipo, id) {
    const grupo = document.createElement("div");
    grupo.className = "campo";
    const etiqueta = document.createElement("label");
    etiqueta.textContent = texto;
    etiqueta.htmlFor = nombre + "-" + id;
    let control;
    if (tipo === "select") {
        control = document.createElement("select");
        const opciones = ["Seleccione una relación", "Familia", "Amigo", "Trabajo", "Otro"];
        for (let i = 0; i < opciones.length; i++) {
            const opcion = document.createElement("option");
            opcion.textContent = opciones[i];
            opcion.value = opciones[i];
            if (i === 0) {
                opcion.value = "";
            }
            control.appendChild(opcion);
        }
    } else {
        control = document.createElement("input");
        control.type = tipo;
    }
    control.id = etiqueta.htmlFor;
    control.name = control.id;
    control.className = nombre;
    control.required = true;
    const error = document.createElement("small");
    error.id = "error-" + control.id;
    error.className = "error";
    error.setAttribute("aria-live", "polite");
    control.setAttribute("aria-describedby", error.id);
    grupo.append(etiqueta, control, error);
    return grupo;
}

function eliminarInvitado(bloque) {
    bloque.remove();
    estado.textContent = "";
    renumerarInvitados();
}

function renumerarInvitados() {
    const bloques = contenedor.querySelectorAll(".invitado");
    for (let i = 0; i < bloques.length; i++) {
        bloques[i].querySelector("h3").textContent = "Invitado " + (i + 1);
        bloques[i].querySelector("button").setAttribute("aria-label", "Eliminar invitado " + (i + 1));
    }
    document.getElementById("total").textContent = "Invitados registrados: " + bloques.length;
}

function mostrarError(campo, mensaje) {
    document.getElementById("error-" + campo.id).textContent = mensaje;
    campo.setAttribute("aria-invalid", "true");
}

function limpiarError(campo) {
    document.getElementById("error-" + campo.id).textContent = "";
    campo.removeAttribute("aria-invalid");
}

function validarObligatorio(campo, mensaje) {
    limpiarError(campo);
    if (campo.value.trim() === "") {
        mostrarError(campo, mensaje);
        return false;
    }
    return true;
}

function validarFormulario() {
    let valido = validarCantidad();
    if (!validarObligatorio(document.getElementById("evento"), "Ingrese el nombre del evento.")) valido = false;
    if (!validarObligatorio(document.getElementById("fecha"), "Seleccione una fecha.")) valido = false;
    if (!validarObligatorio(document.getElementById("lugar"), "Ingrese el lugar del evento.")) valido = false;

    const bloques = contenedor.querySelectorAll(".invitado");
    document.getElementById("error-invitados").textContent = "";
    if (bloques.length === 0) {
        document.getElementById("error-invitados").textContent = "Agregue al menos un invitado antes de guardar.";
        mostrarError(cantidad, "Indique la cantidad y pulse Agregar invitados.");
        valido = false;
    }
    for (let i = 0; i < bloques.length; i++) {
        const nombre = bloques[i].querySelector(".nombre");
        const correo = bloques[i].querySelector(".correo");
        const telefono = bloques[i].querySelector(".telefono");
        const relacion = bloques[i].querySelector(".relacion");
        if (!validarObligatorio(nombre, "Ingrese el nombre del invitado.")) valido = false;
        if (!validarObligatorio(correo, "Ingrese el correo del invitado.")) {
            valido = false;
        } else if (!correo.validity.valid) {
            mostrarError(correo, "Ingrese un correo válido.");
            valido = false;
        }
        if (!validarObligatorio(telefono, "Ingrese el teléfono del invitado.")) {
            valido = false;
        } else {
            // Quita temporalmente los caracteres que no son dígitos para contarlos.
            const digitos = telefono.value.replace(/\D/g, "");
            if (digitos.length < 8) {
                mostrarError(telefono, "El teléfono debe contener al menos 8 dígitos.");
                valido = false;
            }
        }
        if (!validarObligatorio(relacion, "Seleccione una relación.")) valido = false;
    }
    return valido;
}

function generarContenidoTxt() {
    // El total se obtiene del DOM para considerar los bloques eliminados.
    const bloques = contenedor.querySelectorAll(".invitado");
    let contenido = "=== EVENTO: " + document.getElementById("evento").value.trim() + " ===\r\n";
    contenido += "Fecha: " + document.getElementById("fecha").value + "\r\n";
    contenido += "Lugar: " + document.getElementById("lugar").value.trim() + "\r\n";
    contenido += "Total invitados: " + bloques.length + "\r\n";
    for (let i = 0; i < bloques.length; i++) {
        contenido += "\r\n--- INVITADO " + (i + 1) + " ---\r\n";
        contenido += "Nombre: " + bloques[i].querySelector(".nombre").value.trim() + "\r\n";
        contenido += "Correo: " + bloques[i].querySelector(".correo").value.trim() + "\r\n";
        contenido += "Teléfono: " + bloques[i].querySelector(".telefono").value.trim() + "\r\n";
        contenido += "Relación: " + bloques[i].querySelector(".relacion").value + "\r\n";
    }
    return contenido;
}

function descargarArchivo(contenido) {
    const blob = new Blob([contenido], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    // Crea temporalmente un enlace para descargar el archivo sin servidor.
    const enlace = document.createElement("a");
    enlace.href = url;
    enlace.download = "invitados.txt";
    document.body.appendChild(enlace);
    enlace.click();
    document.body.removeChild(enlace);
    URL.revokeObjectURL(url);
}
