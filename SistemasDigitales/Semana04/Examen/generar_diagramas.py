"""Dibujos vectoriales propios; SVG y PNG a 300 DPI, sin servicios externos.

Graphviz se detecta y se utiliza para ordenar los bloques cuando está disponible.
El trazado final usa primitivas vectoriales de Matplotlib (sin gráficos estadísticos).
Si no hay dot, el diseño equivalente se calcula íntegramente en Python.
"""
from pathlib import Path
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch, Rectangle, Circle, Arc
from PIL import Image
from verificar_operaciones import (BASE, N, M, RESULTADO, BIN_N, BIN_M, BIN_S,
                                   agrupar, etapas, acarreos_bits, verificar, exigir)

matplotlib.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'path',
                           'savefig.facecolor': 'white', 'font.size': 12})
NOMBRES = ['problema01_7402_circuito', 'problema02_7483_cascada', 'problema02_suma_binaria']
SECCION = 'ARCHIVOS GRÁFICOS ASOCIADOS'
GENERADOS = []


def detectar_dot():
    candidatos = [shutil.which('dot')]
    for raiz in (os.environ.get('ProgramFiles'), os.environ.get('ProgramFiles(x86)'),
                 str(Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs')):
        if raiz and Path(raiz).exists():
            candidatos.extend(str(p) for p in Path(raiz).glob('Graphviz*/bin/dot.exe'))
    return next((p for p in candidatos if p and Path(p).is_file()), None)


def orden_bloques(dot):
    if dot:
        grafo = 'digraph G { rankdir=LR; ' + ' -> '.join(f'b{i}' for i in range(6)) + '; }'
        try:
            salida = subprocess.run([dot, '-Tplain'], input=grafo, text=True,
                                    capture_output=True, check=True, timeout=30).stdout
            posiciones = [(float(l.split()[2]), int(l.split()[1][1:]))
                          for l in salida.splitlines() if l.startswith('node ')]
            orden = [i for _, i in sorted(posiciones)]
            exigir(orden == list(range(6)), 'Graphviz alteró el orden de etapas')
            return orden, f'Graphviz ({dot}) + composición vectorial Python'
        except (OSError, subprocess.SubprocessError, ValueError) as e:
            print(f'Graphviz no utilizable: {e}; se emplea diseño Python.')
    return list(range(6)), 'Alternativa Python: Matplotlib; dot no disponible/utilizable'


class Lamina:
    def __init__(self, ancho, alto, titulo, subtitulo):
        self.ancho, self.alto = ancho, alto
        self.fig = plt.figure(figsize=(ancho/100, alto/100))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set(xlim=(0, ancho), ylim=(alto, 0), aspect='equal')
        self.ax.axis('off')
        self.textos = []
        self.texto(55, 48, titulo, 22, peso='bold')
        self.texto(55, 85, subtitulo, 11)
        self.linea([(55, 108), (ancho-55, 108)], lw=1)
        self.texto(55, alto-30, 'UNAC · Ingeniería de Sistemas · Sistemas Digitales · Práctica 01', 10)

    def texto(self, x, y, contenido, tam=12, al='left', peso='normal', mono=False):
        t = self.ax.text(x, y, contenido, fontsize=tam, ha=al, va='center',
                         weight=peso, fontfamily='DejaVu Sans Mono' if mono else 'DejaVu Sans')
        self.textos.append(t)
        return t

    def linea(self, puntos, lw=1.6, estilo='-'):
        self.ax.plot(*zip(*puntos), color='black', linewidth=lw, linestyle=estilo)

    def flecha(self, a, b):
        self.ax.annotate('', xy=b, xytext=a,
                         arrowprops={'arrowstyle': '-|>', 'lw': 1.6, 'color': 'black',
                                     'shrinkA': 0, 'shrinkB': 0})

    def caja(self, x, y, w, h, gris=False, estilo='-'):
        self.ax.add_patch(Rectangle((x,y),w,h,fc='#f3f3f3' if gris else 'white',
                                    ec='black',lw=1.4,linestyle=estilo))

    def punto(self, x, y):
        self.ax.add_patch(Circle((x,y), 4, color='black'))

    def guardar(self, nombre):
        self.fig.canvas.draw()
        renderer = self.fig.canvas.get_renderer()
        limites = self.fig.bbox
        for t in self.textos:
            b = t.get_window_extent(renderer)
            exigir(b.x0 >= limites.x0 and b.y0 >= limites.y0 and
                   b.x1 <= limites.x1 and b.y1 <= limites.y1,
                   f'Texto fuera de la lámina: {t.get_text()}')
        for ext in ('svg', 'png'):
            p = BASE / f'{nombre}.{ext}'
            self.fig.savefig(p, dpi=300)
            GENERADOS.append(p)
        plt.close(self.fig)


def nor(l, x, y, nombre, pines, salida):
    # Símbolo OR de curvas Bézier y burbuja de negación. Entradas en y ± 25.
    vertices = [(x,y-55),(x+85,y-55),(x+135,y-35),(x+155,y),
                (x+135,y+35),(x+85,y+55),(x,y+55),
                (x+35,y+20),(x+35,y-20),(x,y-55)]
    codigos = [MPath.MOVETO] + [MPath.CURVE4]*9
    l.ax.add_patch(PathPatch(MPath(vertices,codigos),facecolor='white',edgecolor='black',lw=1.8))
    l.ax.add_patch(Circle((x+163,y),8,fc='white',ec='black',lw=1.8))
    for dy, pin in zip((-25,25),pines):
        l.linea([(x-65,y+dy),(x+20,y+dy)])
        l.texto(x-15,y+dy-15,f'p{pin}',10)
    l.texto(x+75,y,nombre,12,al='center',peso='bold')
    l.linea([(x+171,y),(x+220,y)])
    l.texto(x+196,y-20,f'p{salida}',10,al='center')


def circuito():
    l = Lamina(1600, 1150, '01 / Función lógica con un 7402',
               'Tres compuertas NOR de dos entradas · esquema lógico y asignación DIP-14')
    formulas = [r'$F=\neg[(\overline{X}YZ)+(\overline{X}Y\overline{Z})]$',
                r'$=\neg[\overline{X}Y(Z+\overline{Z})]$',
                r'$=\neg(\overline{X}Y)$',r'$=X+\overline{Y}$']
    l.texto(65, 145, 'SIMPLIFICACIÓN', 11, peso='bold')
    for x, f in zip((65,560,1040,1320),formulas):
        l.texto(x, 197, f, 20)
    l.texto(65,248,'Z y W no intervienen en la función simplificada.',12)
    y=415
    nor(l,230,y,'NOR1',(2,3),1)
    nor(l,680,y,'NOR2',(5,6),4)
    nor(l,1130,y,'NOR3',(8,9),10)
    l.texto(65,y,'Y',17,peso='bold')
    l.linea([(95,y),(140,y)])
    l.linea([(140,y-25),(140,y+25)])
    l.linea([(140,y-25),(165,y-25)])
    l.linea([(140,y+25),(165,y+25)])
    l.punto(140,y)
    l.linea([(450,y),(520,y),(520,y+25),(615,y+25)])
    l.texto(493,y-20,r'$\overline{Y}$',17)
    l.texto(560,320,'X',17,peso='bold')
    l.linea([(580,320),(590,320),(590,y-25),(615,y-25)])
    l.linea([(900,y),(1020,y)])
    l.texto(952,y-20,'T',17)
    l.punto(1020,y)
    l.linea([(1020,y-25),(1020,y+25)])
    l.linea([(1020,y-25),(1065,y-25)])
    l.linea([(1020,y+25),(1065,y+25)])
    l.linea([(1350,y),(1470,y)])
    l.texto(1485,y,'F',17,peso='bold')
    l.texto(305,510,r'NOR1: $\overline{Y}=\overline{(Y+Y)}$',15,al='center')
    l.texto(755,510,r'NOR2: $T=\overline{(X+\overline{Y})}$',15,al='center')
    l.texto(1245,510,r'NOR3: $F=\overline{(T+T)}=X+\overline{Y}$',15,al='center')
    l.linea([(55,565),(1545,565)],lw=1)
    l.texto(65,610,'7402 · DIP-14 · VISTA SUPERIOR',14,peso='bold')
    x, top, w, h = 330,660,260,350
    l.caja(x,top,w,h)
    l.ax.add_patch(Arc((x+w/2,top),50,40,theta1=0,theta2=180,lw=1.5))
    l.ax.add_patch(Circle((x+18,top+20),5,color='black'))
    l.texto(x+w/2,825,'7402',21,al='center',peso='bold')
    l.texto(x+w/2,860,'DIP-14',11,al='center')
    izquierda = [('1Y',r'$\overline{Y}$ → p6'),('1A','Y'),('1B','Y'),
                 ('2Y','T → p8, p9'),('2A','X'),('2B',r'$\overline{Y}$ ← p1'),('GND','GND')]
    derecha = [('VCC','+5 V'),('4Y','libre'),('4B','sin uso'),('4A','sin uso'),
               ('3Y','F'),('3B','T ← p4'),('3A','T ← p4')]
    for i in range(7):
        yy=top+35+i*45
        l.linea([(x-35,yy),(x,yy)])
        l.texto(x+12,yy,str(i+1),11)
        l.texto(x-48,yy,f'{izquierda[i][0]}  ·  {izquierda[i][1]}',12,al='right')
        libre=1 <= i <= 3
        l.linea([(x+w,yy),(x+w+35,yy)],estilo='--' if libre else '-')
        l.texto(x+w-12,yy,str(14-i),11,al='right')
        l.texto(x+w+48,yy,f'{derecha[i][0]}  ·  {derecha[i][1]}',12)
    l.texto(910,683,'CONEXIONES UTILIZADAS',14,peso='bold')
    notas = ['Y → pines 2 y 3; pin 1 → pin 6.',
             'X → pin 5; pin 4 → pines 8 y 9.',
             'Salida F → pin 10.',
             '+5 V → pin 14; GND → pin 7.',
             '3 de 4 NOR utilizadas.',
             'Cuarta NOR fuera del circuito funcional:',
             'pines 11 y 12 sin uso; salida 13 libre.',
             'Trazo discontinuo = puerta no utilizada.',
             'Punto negro = unión eléctrica.']
    for i, texto in enumerate(notas):
        l.texto(910,728+i*35,texto,12)
    l.texto(65,1060,'Las etiquetas de señal del DIP indican las mismas redes que el circuito superior.',12)
    l.guardar(NOMBRES[0])


def cascada(orden):
    l = Lamina(1800, 950, '02 / Suma de 24 bits con seis 7483',
               'Cada bloque suma 4 bits · Cout de cada etapa alimenta Cin de la siguiente')
    l.texto(65,155,f'N = {agrupar(BIN_N)}',18,mono=True)
    l.texto(65,195,f'M = {agrupar(BIN_M)}',18,mono=True)
    l.texto(1200,155,f'N = {N:,}',14)
    l.texto(1200,195,f'M = {M:,}',14)
    l.texto(900,250,'PROPAGACIÓN DEL ACARREO: LSB → MSB',14,al='center',peso='bold')
    l.flecha((110,280),(1690,280))
    for posicion, i in enumerate(orden):
        a,b,ci,s,co = etapas()[i]
        x=100+posicion*270
        l.caja(x,330,210,265)
        l.texto(x+105,355,f'7483-{i+1}',17,al='center',peso='bold')
        l.texto(x+105,388,f'Etapa {i+1} · bits {4*i+3}:{4*i}',11,al='center')
        l.linea([(x+12,408),(x+198,408)],lw=0.8)
        l.texto(x+105,438,f'N = {a:04b}',14,al='center',mono=True)
        l.texto(x+105,472,f'M = {b:04b}',14,al='center',mono=True)
        l.texto(x+105,512,f'S[3:0]={s:04b}',13,al='center',mono=True,peso='bold')
        l.texto(x+12,550,f'Cin={ci}',11)
        l.texto(x+198,550,f'Cout={co}',11,al='right')
        l.linea([(x,570),(x+18,570)],lw=1)
        l.linea([(x+192,570),(x+210,570)],lw=1)
        if i<5:
            l.flecha((x+210,570),(x+270,570))
            l.texto(x+240,545,str(co),12,al='center',peso='bold')
        l.texto(x+105,630,'LSB · inicio' if i==0 else ('MSB · final' if i==5 else f'Bits {4*i+3} a {4*i}'),11,al='center')
    l.flecha((45,570),(100,570))
    l.texto(65,540,'0',12,al='center')
    l.flecha((1660,570),(1725,570))
    l.texto(1710,540,'0',12,al='center')
    l.texto(900,695,'RECONSTRUCCIÓN DEL RESULTADO · MSB → LSB (etapas 6, 5, 4, 3, 2, 1)',14,al='center',peso='bold')
    l.caja(270,730,1260,95,gris=True)
    l.texto(900,777,' | '.join(f'{e[3]:04b}' for e in etapas()[::-1]),23,al='center',mono=True)
    l.texto(900,867,f'{agrupar(BIN_S)}₂ = {RESULTADO:,}₁₀   ·   Cout final = 0',17,al='center')
    l.guardar(NOMBRES[1])


def suma_binaria():
    l = Lamina(1600,800,'03 / Suma binaria completa',
               'Operación de 24 bits · alineación por columnas y acarreos calculados bit a bit')
    l.texto(65,150,'cᵢ es el acarreo que ENTRA a la columna i; c₀ = 0. El acarreo final c₂₄ = 0.',13)
    # Cada columna utiliza la misma coordenada en las cuatro filas.
    xs = [370 + j*38 + (j//4)*28 for j in range(24)]
    carries = acarreos_bits()
    for grupo in range(6):
        centro = (xs[grupo*4]+xs[grupo*4+3])/2
        l.texto(centro,220,f'bits {23-grupo*4}:{20-grupo*4}',10,al='center',mono=True)
    filas = [(285,'cᵢ', ''.join(str(carries[i]) for i in range(23,-1,-1)),14),
             (365,'N',BIN_N,25),(445,'+ M',BIN_M,25),(555,'S',BIN_S,25)]
    for yy, etiqueta, bits, tam in filas:
        l.texto(275,yy,etiqueta,18,al='right',mono=True)
        for xx, bit in zip(xs,bits):
            l.texto(xx,yy,bit,tam,al='center',mono=True,peso='bold' if etiqueta=='S' else 'normal')
    l.linea([(340,495),(xs[-1]+25,495)],lw=2)
    l.texto(800,640,f'{N:,} + {M:,} = {RESULTADO:,}',20,al='center',mono=True)
    l.texto(800,705,'Resultado: '+agrupar(BIN_S)+'₂',17,al='center',mono=True)
    l.guardar(NOMBRES[2])


def respaldar_y_enlazar(archivos):
    backup = BASE / 'backup_txt_originales'
    backup.mkdir(exist_ok=True)
    for p in archivos:
        destino = backup / p.name
        if not destino.exists():
            shutil.copy2(p,destino)
        original = p.read_bytes()
        # Idempotencia: una regeneración nunca duplica la sección ni cambia el respaldo.
        if SECCION.encode('utf-8') not in original:
            alumno = p.name.split('_')[0]
            enlaces = [os.path.relpath(BASE / alumno / f'{nombre}.{ext}',p.parent).replace('\\','/')
                       for nombre in NOMBRES for ext in ('png','svg')]
            extra = '\n\n'+SECCION+'\n'+'\n'.join(enlaces)+'\n'
            with p.open('ab') as salida:
                salida.write(extra.encode('utf-8'))
        exigir(p.read_bytes().startswith(destino.read_bytes()),f'Contenido original alterado: {p}')
        txt = p.read_text(encoding='utf-8-sig')
        exigir(txt.count(SECCION)==1, f'Sección duplicada: {p}')
        for linea in txt.split(SECCION,1)[1].strip().splitlines():
            exigir((p.parent / linea).is_file(), f'Enlace roto: {linea}')


def verificar_imagenes():
    for p in GENERADOS:
        exigir(p.stat().st_size>0,f'Archivo vacío: {p}')
        if p.suffix == '.svg':
            raiz = ET.parse(p).getroot()
            exigir(raiz.tag == '{http://www.w3.org/2000/svg}svg',f'No es SVG: {p}')
        else:
            with Image.open(p) as im:
                exigir(im.format=='PNG',f'No es PNG: {p}')
                exigir(all(abs(d-300)<0.1 for d in im.info.get('dpi',(0,0))),f'DPI incorrecto: {p}')
                im.verify()


def informe(archivos, motor):
    lineas = ['VERIFICACIÓN DE DIAGRAMAS',f'Proyecto: {BASE}',f'Motor: {motor}',
              'Dependencias nuevas instaladas: ninguna en esta ejecución.',
              'Archivos procesados:'] + [str(p.relative_to(BASE)) for p in archivos]
    lineas += ['',f'N = {N}; binario verificado: {agrupar(BIN_N)}',
               f'M = {M}; binario verificado: {agrupar(BIN_M)}',
               f'{N} + {M} = {RESULTADO}: OK',
               f'int("{BIN_S}", 2) = {RESULTADO}: OK',
               f'Resultado: {agrupar(BIN_S)}',
               'F = ¬(X̅Y) = X + Y̅; 16 combinaciones X,Y,Z,W verificadas.',
               'NOR utilizadas: 3 de 4 del 7402; 7483 requeridos: 6.',
               'Cadena completa (LSB a MSB):']
    lineas += [f'Etapa {i}: N={a:04b}, M={b:04b}, Cin={ci}, S={s:04b}, Cout={co}'
               for i,(a,b,ci,s,co) in enumerate(etapas(),1)]
    lineas += ['Acarreos C[24] a C[0]: '+''.join(map(str,acarreos_bits()[::-1])),
               'PNG: integridad y metadatos 300 DPI verificados.',
               'SVG: XML y espacio de nombres verificados.',
               'Todos los textos dentro de los límites del lienzo: verificado al renderizar.',
               'Variantes: copias idénticas por alumno; no se modifican datos ni acarreos.',
               'Respaldo: originales preservados byte a byte; enlaces relativos existentes.',
               '', 'IMÁGENES GENERADAS:']
    lineas += [str(p.relative_to(BASE)) for p in GENERADOS]
    lineas += ['', 'COMANDOS DE REGENERACIÓN (desde la carpeta Examen):',
               'python verificar_operaciones.py', 'python generar_diagramas.py']
    (BASE/'verificacion_diagramas.txt').write_text('\n'.join(lineas)+'\n',encoding='utf-8')
    print(f'Proyecto: {BASE}\nTXT encontrados: {len(archivos)}')
    print(f'PNG generados: {sum(p.suffix==".png" for p in GENERADOS)} (300 DPI)')
    print(f'SVG generados: {sum(p.suffix==".svg" for p in GENERADOS)} (XML válido)')
    print(f'Matemática validada: {N} + {M} = {RESULTADO}; F = X + Y complementada.')
    print(f'Motor: {motor}\nDependencias instaladas: ninguna; Matplotlib y Pillow ya disponibles.')
    print('Regenerar:\npython verificar_operaciones.py\npython generar_diagramas.py')


def main():
    GENERADOS.clear()
    archivos = verificar()
    orden, motor = orden_bloques(detectar_dot())
    circuito()
    cascada(orden)
    suma_binaria()
    for p in archivos:
        carpeta = BASE / p.name.split('_')[0]
        carpeta.mkdir(exist_ok=True)
        for nombre in NOMBRES:
            for ext in ('png','svg'):
                destino=carpeta / f'{nombre}.{ext}'
                shutil.copy2(BASE / destino.name,destino)
                GENERADOS.append(destino)
    verificar_imagenes()
    respaldar_y_enlazar(archivos)
    informe(archivos,motor)


if __name__ == '__main__':
    main()
