# Inicio del constructor

## Entorno Conda e instalación

En Anaconda Prompt, crear el entorno solo si todavía no existe (ya fue creado en este equipo):

```bat
conda create -n pw2-builder python=3.12 -y
conda activate pw2-builder
cd C:\Users\ACER\Downloads\PW2_CallaoLimpio_Builder
python -m pip install -r requirements.txt
```

## Ejecución

```bat
conda activate pw2-builder
cd C:\Users\ACER\Downloads\PW2_CallaoLimpio_Builder
python master_builder.py
```

## Hotkeys globales

- F6: ejecutar un único paso. Durante un paso, otras pulsaciones no se acumulan.
- F7: PAUSAR / REANUDAR. Una instalación npm ya iniciada termina su operación; no se inicia otro paso.
- F8: FINALIZAR SESIÓN y sus procesos. NO usar F8 para una pausa.
- F9: mostrar información del siguiente paso.
- ESC: ABORTAR PASO ACTUAL. No avanza el índice. Revisar el archivo o la terminal y usar el botón Reintentar paso; F6 permanece bloqueado ante errores. La restauración de una edición exige que el archivo siga visible.

## Rutas

Original, solo lectura:

```text
C:\Users\ACER\Documents\GitHub\2026_B\ProgramaciónWeb2\Semana05\proyecto
```

Único proyecto abierto en el Explorer de VS Code durante la grabación:

```text
C:\Users\ACER\Documents\GitHub\2026_B\ProgramaciónWeb2\Semana05\proyecto_tutorial
```

## Procedimiento de inicio

1. Cerrar cualquier sesión anterior del constructor. Tener Node/npm y VS Code instalados. El destino debe estar vacío o no existir; el constructor no borra una construcción anterior.
2. Ejecutar el comando indicado arriba. La GUI queda preparada, sin comenzar automáticamente.
3. Elegir el intervalo fijo por carácter: 0.005, 0.010, 0.015, 0.020, 0.030 o 0.040 segundos.
4. Reiniciar el constructor si ya estaba abierto con una versión anterior. Iniciar la grabación y pulsar F6. El primer paso crea o prepara el destino y abre únicamente esa carpeta en una ventana normal de VS Code, con un perfil y puente local fuera del proyecto. Si aparece la bienvenida, cerrar manualmente su cuadro con la X; no hace falta iniciar sesión.
5. Pulsar F6 o F6 Siguiente cuando corresponda cada nuevo paso. Ambos usan la misma acción. El constructor trae VS Code al frente, activa el archivo y sitúa el cursor antes de editar. TYPE escribe progresivamente y desplaza la vista; INSERT muestra el bloque durante 1,5 segundos y guarda. Los comandos, la limpieza y la creación de archivos se muestran en la terminal integrada de PowerShell. No cambiar de pestaña o ventana durante la escritura; si se pierde el foco, el paso se detiene. Siguiente se deshabilita mientras trabaja y se habilita al volver a LISTO.
6. Seguir los 58 pasos. La GUI muestra tiempo, progreso y adelanto/retraso; no fuerza los 28 minutos de construcción. Los pasos finales verifican archivos, compilan, ejecutan npm run dev y abren Edge para los dos minutos de demostración.
7. Al terminar la demostración, pulsar F8 o cerrar el constructor. Esto también detiene su servidor de desarrollo. Los archivos construidos permanecen en el destino.
