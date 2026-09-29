const formulario = document.getElementById("formulario");
const busqueda = document.getElementById("busqueda");
const boton = document.getElementById("buscar");
const mensaje = document.getElementById("mensaje");
const resultado = document.getElementById("resultado");

// El formulario permite buscar con el botón o con Enter sin recargar la página.
formulario.addEventListener("submit", function (event) {
    event.preventDefault();
    buscarPokemon();
});

async function buscarPokemon() {
    if (boton.disabled) {
        return;
    }

    const nombre = busqueda.value.trim().toLowerCase();
    resultado.hidden = true;
    mensaje.textContent = "";

    if (nombre === "") {
        mensaje.textContent = "Ingrese un nombre o número de Pokémon.";
        return;
    }

    boton.disabled = true;
    mensaje.textContent = "Buscando Pokémon...";

    try {
        // Consulta el nombre o ID como una parte de la URL.
        const url = "https://pokeapi.co/api/v2/pokemon/" + encodeURIComponent(nombre) + "/";
        const respuesta = await fetch(url);

        if (!respuesta.ok) {
            if (respuesta.status === 404) {
                mensaje.textContent = "Pokémon no encontrado.";
            } else {
                mensaje.textContent = "No se pudo consultar la API.";
            }
            return;
        }

        // Convierte el cuerpo JSON de la respuesta en un objeto JavaScript.
        const datos = await respuesta.json();
        mostrarPokemon(datos);
        mensaje.textContent = "";
    } catch (error) {
        mensaje.textContent = "No se pudo consultar la API.";
    } finally {
        // Vuelve a habilitar el botón tanto si hubo éxito como si hubo un error.
        boton.disabled = false;
    }
}

function mostrarPokemon(datos) {
    document.getElementById("nombre").textContent = datos.name;
    document.getElementById("numero").textContent = "N.º " + datos.id;
    document.getElementById("altura").textContent = datos.height + " dm";
    document.getElementById("peso").textContent = datos.weight + " hg";

    const imagen = document.getElementById("imagen");
    const sinImagen = document.getElementById("sin-imagen");
    if (datos.sprites.front_default) {
        imagen.src = datos.sprites.front_default;
        imagen.alt = "Imagen de " + datos.name;
        imagen.hidden = false;
        sinImagen.hidden = true;
    } else {
        imagen.removeAttribute("src");
        imagen.hidden = true;
        sinImagen.hidden = false;
    }

    // Recorre el arreglo y separa los tipos con una barra.
    let tipos = "";
    for (let i = 0; i < datos.types.length; i++) {
        if (i > 0) {
            tipos += " / ";
        }
        tipos += datos.types[i].type.name;
    }
    document.getElementById("tipos").textContent = tipos;
    resultado.hidden = false;
}
