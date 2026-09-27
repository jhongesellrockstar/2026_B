"""Verificación independiente de operandos, acarreos, NOR y solucionarios."""
from pathlib import Path
from itertools import product
import re

BASE = Path(__file__).resolve().parent
N, M, RESULTADO = 7968574, 8694583, 16663157
BIN_N = '011110011001011100111110'
BIN_M = '100001001010101100110111'
BIN_S = '111111100100001001110101'


def exigir(condicion, mensaje):
    if not condicion:
        raise ValueError(mensaje)


def agrupar(bits):
    return ' '.join(bits[i:i+4] for i in range(0, len(bits), 4))


def etapas():
    filas, cin = [], 0
    for i in range(6):
        a, b = (N >> (4*i)) & 15, (M >> (4*i)) & 15
        total = a + b + cin
        filas.append((a, b, cin, total & 15, total >> 4))
        cin = total >> 4
    return filas


def acarreos_bits():
    """C[i] entra a la columna i; C[24] sale de la columna 23."""
    c = [0]
    for i in range(24):
        c.append((((N >> i) & 1) + ((M >> i) & 1) + c[-1]) >> 1)
    return c


def fuentes():
    candidatos = [p for p in BASE.rglob('estudiante*_solucionario.txt')
                  if 'backup_txt_originales' not in p.parts]
    esperados = {f'estudiante{i}_solucionario.txt' for i in range(1, 9)}
    exigir(len(candidatos) == 8 and {p.name for p in candidatos} == esperados,
           'Se necesitan exactamente los ocho solucionarios, sin duplicados.')
    return sorted(candidatos, key=lambda p: p.name)


def verificar():
    exigir(N + M == RESULTADO, 'Suma decimal incorrecta')
    for valor, bits in [(N, BIN_N), (M, BIN_M), (RESULTADO, BIN_S)]:
        exigir(format(valor, '024b') == bits and int(bits, 2) == valor,
               f'Conversión incorrecta: {valor}')
    esperado = [(14,7,0,5,1),(3,3,1,7,0),(7,11,0,2,1),
                (9,10,1,4,1),(9,4,1,14,0),(7,8,0,15,0)]
    exigir(etapas() == esperado, 'Cadena de nibbles incorrecta')
    exigir(''.join(f'{e[3]:04b}' for e in etapas()[::-1]) == BIN_S,
           'Reconstrucción incorrecta')
    c = acarreos_bits()
    suma = 0
    for i in range(24):
        total = ((N >> i) & 1) + ((M >> i) & 1) + c[i]
        exigir(total >> 1 == c[i+1], f'Acarreo incorrecto en bit {i}')
        suma |= (total & 1) << i
    exigir(suma == RESULTADO and c[24] == 0, 'Suma bit a bit incorrecta')
    for i, fila in enumerate(etapas()):
        exigir((c[4*i], c[4*i+4]) == (fila[2], fila[4]), 'Acarreo de bloque incorrecto')
    for x, y, z, w in product((0, 1), repeat=4):
        original = not (((not x) and y and z) or ((not x) and y and (not z)))
        ybar = not (y or y)
        t = not (x or ybar)
        f = not (t or t)
        exigir(original == f == bool(x or not y), f'Fallo NOR: {x,y,z,w}')
    revision = ['REVISIÓN DE CÁLCULOS', 'No se encontraron discrepancias en los ocho originales.',
                'Los textos originales se conservan; solo se agregan enlaces a gráficos.', '']
    for p in fuentes():
        txt = p.read_text(encoding='utf-8-sig')
        requeridos = [f'N = {N}', f'M = {M}', f'N = {agrupar(BIN_N)}',
                      f'M = {agrupar(BIN_M)}', f'Resultado decimal: {RESULTADO}',
                      f'Resultado binario: {BIN_S}', f'Resultado agrupado: {agrupar(BIN_S)}',
                      'F = X + Y̅', 'Y̅ = NOR(Y,Y)', 'T = NOR(X,Y̅)', 'F = NOR(T,T)',
                      'VCC pin 14, GND pin 7', 'N = 0x79973E', 'M = 0x84AB37', 'S = 0xFE4275']
        for valor in requeridos:
            exigir(valor in txt, f'{p.name}: falta o difiere {valor!r}')
        for i, (a,b,ci,s,co) in enumerate(etapas(), 1):
            detalle = f'E{i}: {a} + {b} + {ci} = {a+b+ci} -> salida {s:04b}, acarreo {co}'
            exigir(detalle in txt, f'{p.name}: detalle incorrecto en etapa {i}')
            if 'Etapa 1:' in txt:
                exigir(f'Etapa {i}: {a:04b} + {b:04b} + Cin({ci}) = {s:04b}, Cout = {co}' in txt,
                       f'{p.name}: etapa {i} incorrecta')
            else:
                patron = rf'^\s*{i}\s*\|\s*{a:04b}\s*\|\s*{b:04b}\s*\|\s*{ci}\s*\|\s*{s:04b}\s*\|\s*{co}\s*$'
                exigir(re.search(patron, txt, re.M) is not None, f'{p.name}: tabla incorrecta')
        revision.append(f'OK: {p.relative_to(BASE)} — datos, seis etapas y resultado coinciden.')
    (BASE / 'revision_calculos.txt').write_text('\n'.join(revision)+'\n', encoding='utf-8')
    return fuentes()


if __name__ == '__main__':
    archivos = verificar()
    print(f'Proyecto: {BASE}\nTXT encontrados: {len(archivos)}')
    print(f'{N} + {M} = {RESULTADO}\nBinario: {agrupar(BIN_S)}')
    print('NOR: 16 combinaciones verificadas; F = X + Y complementada.')
    print('Seis 7483; Cin/Cout: ' + ', '.join(f'{e[2]}/{e[4]}' for e in etapas()))
