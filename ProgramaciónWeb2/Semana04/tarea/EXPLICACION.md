# Cómo funciona el Buscador de Pokémon

Esta práctica consume una API externa. No crea una API ni necesita una base de datos propia. Abre `index.html` en Edge con conexión a Internet; los otros dos archivos deben permanecer en la misma carpeta.

## API, REST y endpoint

Una **API** es una forma definida de pedir información o servicios a otro programa. **REST** es un estilo para organizar servicios web alrededor de recursos y operaciones HTTP: por ejemplo, una petición GET consulta un recurso identificado por una URL.

**PokéAPI** es una API pública con información de Pokémon. Un **endpoint** es una dirección de la API que permite consultar un recurso. Usamos:

```text
https://pokeapi.co/api/v2/pokemon/{nombre o ID}/
https://pokeapi.co/api/v2/pokemon/pikachu/
https://pokeapi.co/api/v2/pokemon/25/
```

Las dos últimas direcciones consultan a Pikachu. No necesitamos una clave de acceso.

## Del formulario a la consulta

El evento `submit` ocurre al pulsar Buscar o Enter. `event.preventDefault()` evita que el formulario recargue la página. Después llama a `buscarPokemon()`.

```javascript
const nombre = busqueda.value.trim().toLowerCase();
```

`value` obtiene el texto; `trim()` quita espacios al principio y al final; `toLowerCase()` convierte las letras a minúsculas. Si no queda texto, mostramos un mensaje y `return` termina la función sin consultar la API.

```javascript
const url = "https://pokeapi.co/api/v2/pokemon/" + encodeURIComponent(nombre) + "/";
const respuesta = await fetch(url);
```

`encodeURIComponent()` evita que caracteres como `/` o `?` escritos en el campo cambien la estructura de la dirección. `fetch()` inicia una petición HTTP GET y devuelve una **promesa**: representa un resultado que llegará después. `await` espera ese resultado dentro de una función `async`, sin bloquear toda la página.

El resultado es un objeto **Response**, guardado aquí como `respuesta`. Contiene el estado HTTP y permite leer el cuerpo de la respuesta; todavía no es el objeto con los datos del Pokémon.

## De Response a un objeto JavaScript

`respuesta.ok` es verdadero si el estado HTTP está entre 200 y 299. Un error HTTP como 404 no hace que `fetch()` entre automáticamente en `catch`, por eso lo comprobamos con `if`.

```javascript
const datos = await respuesta.json();
```

**JSON** es un formato de texto para representar datos mediante propiedades, valores y arreglos. El método `.json()` lee e interpreta ese texto; también devuelve una promesa. Después de `await`, `datos` es un objeto JavaScript cuyas propiedades podemos consultar con un punto.

| Código | Información |
| --- | --- |
| `datos.name` | Nombre, por ejemplo `pikachu` |
| `datos.id` | Identificador, por ejemplo `25` |
| `datos.height` | Altura en decímetros: `4 dm` equivale a `0.4 m` |
| `datos.weight` | Peso en hectogramos: `60 hg` equivale a `6 kg` |
| `datos.sprites` | Objeto con direcciones de imágenes |
| `datos.sprites.front_default` | URL del sprite frontal, o `null` si no hay imagen |
| `datos.types` | Arreglo de tipos |
| `datos.types[0].type.name` | Nombre del primer tipo |

Conservamos los valores de altura y peso que entrega la API y mostramos sus unidades.

## Del objeto a la página

El **DOM** representa los elementos del HTML. `mostrarPokemon(datos)` busca esos elementos por su ID y actualiza sus contenidos:

```javascript
document.getElementById("nombre").textContent = datos.name;
document.getElementById("numero").textContent = "N.º " + datos.id;
```

`textContent` coloca texto sin interpretarlo como HTML. Para la imagen usamos `imagen.src = datos.sprites.front_default`; su dirección procede del JSON, no de una imagen guardada en el proyecto. Si no existe sprite, mostramos “Imagen no disponible”.

```javascript
let tipos = "";
for (let i = 0; i < datos.types.length; i++) {
    if (i > 0) {
        tipos += " / ";
    }
    tipos += datos.types[i].type.name;
}
```

El ciclo recorre desde la posición cero hasta la última. A partir del segundo tipo agrega una barra: Bulbasaur muestra `grass / poison`. Finalmente se asigna el texto a `tipos` en el HTML y `resultado.hidden = false` hace visible la tarjeta.

## Errores y búsquedas consecutivas

- Campo vacío: “Ingrese un nombre o número de Pokémon.”
- Estado 404: “Pokémon no encontrado.”
- Otro error HTTP, fallo de conexión o JSON que no pueda leerse: “No se pudo consultar la API.”

`try` contiene la consulta; `catch` maneja los fallos; `finally` vuelve a habilitar Buscar incluso cuando se ejecuta un `return` dentro del `try`. Durante la espera el botón está deshabilitado para evitar consultas simultáneas. Al comenzar otra búsqueda se oculta la tarjeta anterior.

## Repaso antes de clase

Prueba `pikachu`, `25`, `bulbasaur`, ` PIKACHU `, el campo vacío y `pokemonquenoexiste12345`. Comprueba que Bulbasaur tenga dos tipos y que la tarjeta anterior desaparezca al fallar otra consulta. Abre F12 → Consola para revisar errores JavaScript; un 404 de red al buscar un nombre inexistente es una respuesta esperada de la API.

Para reproducir el ejercicio: crea el formulario, registra `submit`, valida el texto, llama a `fetch()`, comprueba `ok`, lee `.json()` y asigna las propiedades a los elementos del HTML.

Referencias: [Fetch API en W3Schools](https://www.w3schools.com/js/js_api_fetch.asp), [documentación de PokéAPI](https://pokeapi.co/docs/v2) y [Response.ok en MDN](https://developer.mozilla.org/en-US/docs/Web/API/Response/ok).
