"""Compila ocho solucionarios con XeLaTeX reutilizando los PNG existentes.

Ejecutar: python generar_entrega_final.py
Dependencias Python: Pillow, PyMuPDF. Motor externo: xelatex (MiKTeX/TeX Live).
No modifica ni elimina fuentes; los auxiliares permanecen en el archivo de trabajo.
"""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys

from PIL import Image
import fitz

BASE = Path(__file__).resolve().parent
FINAL = BASE / 'ENTREGA_FINAL'
ARCHIVO = FINAL / '_ARCHIVO_TRABAJO_PREVIO'
FUENTES = BASE / 'solucionarios_8_estudiantes_sistemas_digitales'
N, M, S = 7968574, 8694583, 16663157
BN, BM, BS = ('0111 1001 1001 0111 0011 1110',
              '1000 0100 1010 1011 0011 0111',
              '1111 1110 0100 0010 0111 0101')
GRAFICOS = ['problema01_7402_circuito','problema02_7483_cascada','problema02_suma_binaria']


def exigir(condicion, mensaje):
    if not condicion:
        raise RuntimeError(mensaje)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def etapas():
    filas, cin = [], 0
    for i in range(6):
        a, b = (N >> (4*i)) & 15, (M >> (4*i)) & 15
        total = a+b+cin
        filas.append((a,b,cin,total & 15,total >> 4))
        cin = total >> 4
    return filas


def revisar_fuentes():
    exigir(N+M == S == int(BS.replace(' ',''),2), 'Suma incorrecta')
    exigir(int(BN.replace(' ',''),2)==N and int(BM.replace(' ',''),2)==M,'Conversión incorrecta')
    for x in (0,1):
        for y in (0,1):
            for z in (0,1):
                f = not (((not x) and y and z) or ((not x) and y and not z))
                yb = not (y or y)
                t = not (x or yb)
                exigir(f == (not(t or t)) == bool(x or not y),'Ecuación NOR incorrecta')
    fuentes = []
    for i in range(1,9):
        p = FUENTES / f'estudiante{i}_solucionario.txt'
        texto = p.read_text(encoding='utf-8-sig')
        for s in (str(N),str(M),str(S),BN,BM,BS,'F = X + Y̅'):
            exigir(s in texto, f'No coincide {s}: {p}')
        for j,(a,b,ci,s,co) in enumerate(etapas(),1):
            exigir(f'E{j}: {a} + {b} + {ci} = {a+b+ci} -> salida {s:04b}, acarreo {co}' in texto,
                   f'Etapa {j} incorrecta en {p}')
        fuentes.append(p)
    return fuentes


def archivar():
    # Lista explícita: nunca recorrer ni copiar ENTREGA_FINAL dentro de sí misma.
    grupos = {
        'scripts': ['generar_diagramas.py','verificar_operaciones.py','requirements.txt'],
        'diagramas_raiz': [f'{n}.{e}' for n in GRAFICOS for e in ('png','svg')],
        'verificaciones': ['control_calidad_visual.txt','revision_calculos.txt',
                          'verificacion_diagramas.txt','LEEME_diagramas.txt'],
        'otros': ['Captura de pantalla 2026-09-22 155914.png',
                  'WhatsApp Image 2026-09-22 at 3.36.11 PM.jpeg'],
    }
    manifiesto = []
    for grupo, nombres in grupos.items():
        carpeta=ARCHIVO/grupo
        carpeta.mkdir(parents=True,exist_ok=True)
        for nombre in nombres:
            origen=BASE/nombre
            exigir(origen.is_file(),f'Falta archivo para preservar: {origen}')
            destino=carpeta/nombre
            shutil.copy2(origen,destino)
            exigir(sha(origen)==sha(destino),f'Copia no idéntica: {nombre}')
            manifiesto.append({'original':str(origen.relative_to(BASE)),
                              'archivo':str(destino.relative_to(FINAL)),'sha256':sha(origen)})
    (ARCHIVO/'verificaciones'/'manifiesto_archivado.json').write_text(
        json.dumps(manifiesto,ensure_ascii=False,indent=2),encoding='utf-8')


def escapar(s):
    tabla = {'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$',
             '#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(tabla.get(c,c) for c in s)


def imagen(p, ancho='\\linewidth', region=None):
    """Recorte solo de presentación en LaTeX: no crea un nuevo PNG.

    region usa coordenadas normalizadas (izquierda, arriba, derecha, abajo).
    Se conserva el archivo original y su resolución de 300 DPI.
    """
    with Image.open(p) as im:
        im.verify()
    with Image.open(p) as im:
        w,h = im.size
        dx,dy=im.info.get('dpi',(300,300))
    opciones=f'width={ancho}'
    if region:
        l,t,r,b=region
        recorte=(l*w*72/dx,(1-b)*h*72/dy,(1-r)*w*72/dx,t*h*72/dy)
        opciones+=',trim={'+' '.join(f'{v:.4f}bp' for v in recorte)+'},clip'
    return r'\includegraphics['+opciones+']{'+p.as_posix()+'}'


def documento(i):
    fuente=FUENTES/f'estudiante{i}_solucionario.txt'
    texto=fuente.read_text(encoding='utf-8-sig')
    metodo=re.search(r'Método:\s*(.+)',texto).group(1)
    enfoque=texto.split('Método:',1)[1].splitlines()[1].strip()
    identidad=f'Estudiante {i}'+(': Jhon Gesell' if i==5 else '')
    carpeta=BASE/f'estudiante{i}'
    p1,p2,p3=[carpeta/f'{n}.png' for n in GRAFICOS]
    # Los PNG han sido validados previamente; no es necesario convertir SVG ni regenerar.
    logica=imagen(p1,region=(.032,.265,.963,.470))
    dip=imagen(p1,ancho='110mm',region=(.055,.560,.530,.892))
    cascada1=imagen(p2,ancho='148mm',region=(.020,.340,.500,.680))
    cascada2=imagen(p2,ancho='145mm',region=(.496,.340,.966,.680))
    suma=imagen(p3,region=(.125,.230,.935,.735))
    filas=[]
    for j,(a,b,ci,s,co) in enumerate(etapas(),1):
        filas.append(f'7483-{j} & {4*j-1}:{4*j-4} & \\texttt{{{a:04b}}} & \\texttt{{{b:04b}}} & {ci} & \\texttt{{{s:04b}}} & {co} \\\\')
    cuerpo=r'''\documentclass[10pt,a4paper]{article}
\usepackage[margin=16mm,headheight=14pt,headsep=6mm,footskip=9mm]{geometry}
\usepackage{fontspec}
\setmainfont{TeX Gyre Pagella}
\setsansfont{TeX Gyre Heros}
\setmonofont{Latin Modern Mono}
\usepackage{amsmath,amssymb,graphicx,booktabs,array,fancyhdr}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small Sistemas Digitales / Práctica 01}
\fancyhead[R]{\small @@IDENTIDAD@@}
\fancyfoot[L]{\small Universidad Nacional del Callao}
\fancyfoot[R]{\small \thepage\ / 4}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\renewcommand{\arraystretch}{1.22}
\newcommand{\titulo}[1]{\par\vspace{3pt}{\Large\sffamily\bfseries #1}\par\vspace{4pt}}
\newcommand{\subtitulo}[1]{\par\vspace{5pt}{\bfseries\sffamily #1}\par}
\newcommand{\respuesta}[1]{\par\vspace{4pt}\noindent\fbox{\parbox{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}{#1}}\par}
\begin{document}
{\sffamily\bfseries UNIVERSIDAD NACIONAL DEL CALLAO}\par
Ingeniería de Sistemas\hfill Curso: Sistemas Digitales\par
\textbf{Práctica 01}\hfill \textbf{@@IDENTIDAD@@}
\titulo{Pregunta 1 / Reducción booleana}
\textbf{Enunciado.} Simplificar la función y realizarla únicamente con las puertas NOR de dos entradas de un integrado 7402:
\[
F(X,Y,Z,W)=\operatorname{NOR}(\overline X YZ,\overline X Y\overline Z)
=\overline{(\overline X YZ)+(\overline X Y\overline Z)}.
\]
\textbf{@@METODO@@.} @@ENFOQUE@@
\subtitulo{Procedimiento}
Se factoriza el término común y se aplica la complementariedad de $Z$:
\begin{align*}
P&=\overline X YZ+\overline X Y\overline Z\\
 &=\overline X Y(Z+\overline Z) &&\text{factor común}\\
 &=\overline X Y(1)=\overline X Y &&\text{complementariedad}.
\end{align*}
La salida NOR niega $P$. Por De Morgan y doble negación:
\[
F=\overline P=\overline{\overline X Y}
=\overline{\overline X}+\overline Y
=\boxed{X+\overline Y}.
\]
Las variables $Z$ y $W$ no intervienen en la función reducida.
\subtitulo{Realización con tres NOR del 7402}
\begin{center}
\begin{tabular}{lll}\toprule
Puerta & Operación & Señal obtenida\\\midrule
NOR1 & $\operatorname{NOR}(Y,Y)$ & $\overline Y=\overline{Y+Y}$\\
NOR2 & $\operatorname{NOR}(X,\overline Y)$ & $T=\overline{X+\overline Y}$\\
NOR3 & $\operatorname{NOR}(T,T)$ & $F=\overline{T+T}=X+\overline Y$\\\bottomrule
\end{tabular}
\end{center}
@@LOGICA@@
{\small Circuito original reutilizado. Los puntos negros indican uniones; cada burbuja de salida indica negación. La asignación ampliada de pines está en la página 2.}
\respuesta{\textbf{Frase para transcribir.} La función se simplifica a $F=X+\overline Y$. Se implementa con tres de las cuatro puertas NOR del 7402: una invierte $Y$, otra obtiene $T$ y la tercera invierte $T$.}
\newpage
\titulo{Pregunta 1 / Pines y comprobación}
\textbf{Montaje funcional.} El encapsulado DIP-14 se observa desde arriba. La muesca y el punto de referencia permiten localizar el pin 1.
\begin{center}@@DIP@@\end{center}
\subtitulo{Conexiones listas para cablear}
\begin{center}
\begin{tabular}{p{34mm}p{128mm}}\toprule
Red o puerta & Pines y conexión\\\midrule
NOR1 & $Y$ a 2 (1A) y 3 (1B); salida 1 (1Y): $\overline Y$.\\
NOR2 & $X$ a 5 (2A); 1 a 6 (2B); salida 4 (2Y): $T$.\\
NOR3 & 4 a 8 (3A) y 9 (3B); salida 10 (3Y): $F$.\\
Alimentación & Pin 14 (VCC) a $+5\,\mathrm V$; pin 7 (GND) a tierra.\\
NOR4 & 11 (4A), 12 (4B) y 13 (4Y): puerta no utilizada en esta función.\\\bottomrule
\end{tabular}
\end{center}
\subtitulo{Comprobación de la red NOR}
\begin{center}
\begin{tabular}{cccccc}\toprule
$X$ & $Y$ & $\overline Y$ & $T=\overline{X+\overline Y}$ & $F=\overline T$ & $X+\overline Y$\\\midrule
0 & 0 & 1 & 0 & 1 & 1\\
0 & 1 & 0 & 1 & 0 & 0\\
1 & 0 & 1 & 0 & 1 & 1\\
1 & 1 & 0 & 0 & 1 & 1\\\bottomrule
\end{tabular}
\end{center}
Cada fila es válida para cualquier valor de $Z$ y $W$. La salida de las tres NOR coincide con la ecuación simplificada.
\respuesta{\textbf{Resultado de la Pregunta 1:} $\boxed{F=X+\overline Y}$. Se utiliza un integrado 7402, con tres puertas activas y una disponible.}
\newpage
\titulo{Pregunta 2 / Suma con seis 7483}
\textbf{Datos:} $N=7{,}968{,}574$ y $M=8{,}694{,}583$.
\subtitulo{Conversión y organización de 24 bits}
La conversión hexadecimal permite revisar grupos de cuatro bits:
\[
N=\texttt{79973E}_{16},\qquad M=\texttt{84AB37}_{16}.
\]
Cada dígito hexadecimal se sustituye por un nibble, conservando los ceros iniciales:
\begin{center}\begin{tabular}{rl}
$N=$ & \texttt{0111 1001 1001 0111 0011 1110}\\
$M=$ & \texttt{1000 0100 1010 1011 0011 0111}
\end{tabular}\end{center}
Se requieren $24/4=\mathbf{6}$ sumadores 7483. Se comienza por los bits 3:0 con $C_{\mathrm{in}}=0$. Cada $C_{\mathrm{out}}$ alimenta el $C_{\mathrm{in}}$ de la siguiente etapa.
\subtitulo{Tabla de etapas: desde LSB hacia MSB}
\begin{center}
\begin{tabular}{ccccccc}\toprule
Bloque & Bits & Nibble $N$ & Nibble $M$ & $C_{\mathrm{in}}$ & $S[3:0]$ & $C_{\mathrm{out}}$\\\midrule
@@FILAS@@
\bottomrule\end{tabular}\end{center}
En el primer bloque: $14+7+0=21=16+5$; se entrega $0101$ y acarreo 1.
\subtitulo{Cascada ampliada: dos tramos del mismo circuito}
{\small Tramo A: etapas 1--3. El bloque 1 procesa los bits menos significativos.}\par
\centerline{@@CASCADA1@@}
\begin{center}\small\textbf{Tramo B: $C_{\mathrm{out},3}=1\ \longrightarrow\ C_{\mathrm{in},4}=1$. Final: $C_{\mathrm{out},6}=0$.}\end{center}
\centerline{@@CASCADA2@@}
\newpage
\titulo{Pregunta 2 / Suma y resultado final}
\subtitulo{Suma binaria completa}
En la fila $c_i$ se muestra el acarreo que entra a la columna $i$. El bit 0 está a la derecha. Se parte de $c_0=0$ y se obtiene $c_{24}=0$.
\begin{center}@@SUMA@@\end{center}
\subtitulo{Reconstrucción en orden MSB a LSB}
Las salidas se leen de la etapa 6 a la 1, en orden inverso al avance del acarreo:
\begin{center}
\begin{tabular}{cccccc}\toprule
Etapa 6 & Etapa 5 & Etapa 4 & Etapa 3 & Etapa 2 & Etapa 1\\\midrule
\texttt{1111} & \texttt{1110} & \texttt{0100} & \texttt{0010} & \texttt{0111} & \texttt{0101}\\\bottomrule
\end{tabular}
\end{center}
\[
S=\texttt{1111 1110 0100 0010 0111 0101}_{2}
=16{,}663{,}157_{10}.
\]
\subtitulo{Comprobación decimal y hexadecimal}
\[
7{,}968{,}574+8{,}694{,}583=\boxed{16{,}663{,}157},
\qquad S=\texttt{FE4275}_{16}.
\]
No se produce acarreo fuera de los 24 bits: el $C_{\mathrm{out}}$ del sexto bloque es 0.
\respuesta{\textbf{Frase para transcribir.} Se utilizan seis sumadores 7483 en cascada, desde el nibble menos significativo. La suma es \texttt{1111 1110 0100 0010 0111 0101} en base 2, equivalente a \textbf{16,663,157} en decimal.}
\subtitulo{Resumen final}
\begin{center}\begin{tabular}{ll}\toprule
Pregunta 1 & $F=X+\overline Y$; tres NOR del 7402.\\
Pregunta 2 & $N+M=16{,}663{,}157$; seis 7483.\\
Binario & \texttt{1111 1110 0100 0010 0111 0101}$_2$.\\\bottomrule
\end{tabular}\end{center}
{\small Fuente: solucionario individual del estudiante y diagramas originales de su carpeta. Se conservan los datos, los pines y los acarreos.}
\end{document}
'''
    valores={'IDENTIDAD':escapar(identidad),'METODO':escapar(metodo),'ENFOQUE':escapar(enfoque),
             'LOGICA':logica,'DIP':dip,'CASCADA1':cascada1,'CASCADA2':cascada2,
             'SUMA':suma,'FILAS':'\n'.join(filas)}
    for clave,valor in valores.items():
        cuerpo=cuerpo.replace('@@'+clave+'@@',valor)
    return cuerpo


def validar_pdf(pdf, i, log):
    exigir(pdf.is_file() and pdf.stat().st_size>0,f'PDF ausente: {pdf}')
    exigir(not re.search(r'Overfull \\[hv]box|Missing character:|^!',log,re.M),'Error de maquetación en '+str(pdf))
    with fitz.open(pdf) as doc:
        exigir(len(doc)==4,f'Se esperaban 4 páginas, hay {len(doc)}: {pdf}')
        texto='\n'.join(p.get_text() for p in doc)
        plano=' '.join(texto.split())
        for token in ('Pregunta 1','Pregunta 2','16,663,157',BS):
            exigir(token in plano,f'Falta {token} en PDF {i}')
        exigir(all(f'7483-{j}' in texto for j in range(1,7)),f'Tabla incompleta: {i}')
        exigir('F = X + Y' in plano,'Resultado booleano no extraíble')
        exigir(not any(c in texto for c in ('\ufffd','\u25a0','Ã','Â')),'Unicode corrupto')
        if i==5:
            exigir('Estudiante 5: Jhon Gesell' in plano,'Falta identificación exacta')
        for pagina in doc:
            exigir(len(pagina.get_text().strip())>150,'Página vacía o sin contenido')
            # Márgenes de contenido, incluyendo texto e imágenes; tolerancia al pie de página.
            for bloque in pagina.get_text('dict')['blocks']:
                caja=fitz.Rect(bloque['bbox'])
                exigir(caja.x0>=35 and caja.x1<=pagina.rect.width-35 and
                       caja.y0>=12 and caja.y1<=pagina.rect.height-12,
                       f'Contenido fuera de margen en página {pagina.number+1}: {caja}')
        return {'estudiante':i,'paginas':len(doc),'bytes':pdf.stat().st_size,
                'contenido':'OK','margenes':'OK','sha256':sha(pdf)}


def main():
    motor=shutil.which('xelatex')
    if not motor:
        candidato=Path.home()/'AppData/Local/Programs/MiKTeX/miktex/bin/x64/xelatex.exe'
        motor=str(candidato) if candidato.exists() else None
    exigir(motor,'XeLaTeX no se encontró en PATH ni en la ubicación habitual de MiKTeX.')
    fuentes=revisar_fuentes()
    # Fotografías, SVG y fuentes existentes se preservan sin modificación.
    preservados=[p for p in BASE.rglob('*') if p.is_file() and FINAL not in p.parents
                 and '__pycache__' not in p.parts]
    hashes={p:sha(p) for p in preservados}
    archivar()
    qa=[]
    for i,fuente in enumerate(fuentes,1):
        trabajo=ARCHIVO/'scripts'/'compilacion'/f'estudiante{i}'
        trabajo.mkdir(parents=True,exist_ok=True)
        tex=trabajo/'solucionario_final.tex'
        tex.write_text(documento(i),encoding='utf-8')
        print(f'Compilando estudiante {i}...',flush=True)
        cmd=[motor,'-interaction=nonstopmode','-halt-on-error','-file-line-error',tex.name]
        proceso=subprocess.run(cmd,cwd=trabajo,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                               encoding='utf-8',errors='replace',timeout=240)
        (trabajo/'compilacion.txt').write_text(proceso.stdout,encoding='utf-8')
        exigir(proceso.returncode==0,'Falló XeLaTeX: '+str(trabajo/'compilacion.txt')+'\n'+proceso.stdout[-3500:])
        log=tex.with_suffix('.log').read_text(encoding='utf-8',errors='replace')
        pdf=tex.with_suffix('.pdf')
        qa.append(validar_pdf(pdf,i,log))
        destino=FINAL/f'estudiante{i}'
        destino.mkdir(exist_ok=True)
        shutil.copy2(pdf,destino/pdf.name)
        shutil.copy2(fuente,destino/fuente.name)
        exigir(sha(fuente)==sha(destino/fuente.name),'TXT no idéntico a fuente principal')
    exigir(all(sha(p)==valor for p,valor in hashes.items()),'Se alteró un archivo previo')
    for i in range(1,9):
        esperados={'solucionario_final.pdf',f'estudiante{i}_solucionario.txt'}
        exigir({p.name for p in (FINAL/f'estudiante{i}').iterdir()}==esperados,
               f'Archivos inesperados en carpeta de entrega {i}')
    fecha=datetime.now().astimezone().isoformat(timespec='seconds')
    readme=f'''ENTREGA FINAL - PRÁCTICA 01 - SISTEMAS DIGITALES
Generación: {fecha}
Motor LaTeX: {motor}

Hay 8 solucionarios individuales, de 4 páginas cada uno.
Cada estudianteN/ contiene únicamente solucionario_final.pdf y su TXT individual.
Estudiante 5: Jhon Gesell.
No se generaron PNG resumen para mantener la entrega sencilla.

Contenido del PDF:
1. Pregunta 1: función, procedimiento, De Morgan y circuito NOR.
2. Pregunta 1: DIP-14 ampliado, conexiones y tabla de comprobación.
3. Pregunta 2: operandos, conversión, seis etapas y cascada ampliada en dos tramos.
4. Pregunta 2: suma con acarreos, resultado y resumen final.

Fuentes originales (en la carpeta Examen, un nivel arriba):
solucionarios_8_estudiantes_sistemas_digitales/estudianteN_solucionario.txt
estudianteN/problema01_7402_circuito.png
estudianteN/problema02_7483_cascada.png
estudianteN/problema02_suma_binaria.png
backup_txt_originales/ sigue siendo SOLO respaldo, no fuente primaria.
Los TXT finales son copias exactas. Sus referencias gráficas antiguas corresponden
a su ubicación original; para ver la solución integrada se debe abrir el PDF.

Regenerar desde Examen:
python generar_entrega_final.py
Dependencias Python: Pillow y PyMuPDF; XeLaTeX debe estar disponible.
El script reutiliza los PNG y no regenera la colección de diagramas.

_ARCHIVO_TRABAJO_PREVIO contiene copias verificadas del material suelto.
Se copiaron los archivos; no se borraron ni movieron los originales.
No se archivaron carpetas de fuentes ni ENTREGA_FINAL dentro de sí misma.
Los .tex, registros de compilación y PDF intermedios están en scripts/compilacion/.
Los controles automáticos y el manifiesto SHA-256 están en verificaciones/.
Las vistas de revisión están en verificaciones/vistas/ y no son PNG resumen.
'''
    (FINAL/'README_ENTREGA.txt').write_text(readme,encoding='utf-8')
    (ARCHIVO/'verificaciones'/'control_entrega_final.json').write_text(
        json.dumps({'fecha':fecha,'motor':motor,'pdf':qa,'txt_identicos':8,
                    'archivos_previos_sin_cambios':len(hashes),'png_resumen':0},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'\nENTREGA FINAL GENERADA\nRuta: {FINAL}\nEstudiantes: 8\nPDF generados: 8\nTXT copiados: 8\nPNG resumen: 0\nLaTeX utilizado: {motor}\nEstudiante 5: Jhon Gesell [OK]\nPregunta 1 verificada [OK]\nPregunta 2 verificada [OK]\n\npython generar_entrega_final.py')


if __name__=='__main__':
    try:
        main()
    except (RuntimeError,subprocess.TimeoutExpired) as error:
        print(str(error),file=sys.stderr)
        sys.exit(1)
