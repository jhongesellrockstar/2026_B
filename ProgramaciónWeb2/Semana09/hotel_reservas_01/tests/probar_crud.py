"""Prueba local del CRUD real en Apache. No necesita paquetes de Python."""
from pathlib import Path
from http.cookiejar import CookieJar
from urllib.request import Request, build_opener, HTTPCookieProcessor
from urllib.error import HTTPError
from urllib.parse import urlencode
import json,re,subprocess,uuid

ROOT=Path(__file__).resolve().parents[1]
BASE='http://localhost/hotel_reservas_01/public/'
client=build_opener(HTTPCookieProcessor(CookieJar()))
results=[]
def sql(query):
    return subprocess.check_output(['C:/xampp/mysql/bin/mysql.exe','-u','root','--default-character-set=utf8mb4','-N','-B','hotel_reservas_01','-e',query],encoding='utf-8').strip()
def request(req):
    try:
        with client.open(req,timeout=10) as r: return r.status,r.read()
    except HTTPError as r: return r.code,r.read()
def get(path): return request(BASE+path)
def post(path,data,source,csrf=True):
    values=dict(data)
    if csrf:
        body=get(source)[1]; token=re.search(rb'name="csrf_test_name" value="([^"]+)"',body)
        assert token,body[:200]
        values['csrf_test_name']=token[1].decode()
    return request(Request(BASE+path,data=urlencode(values).encode(),headers={'Referer':BASE+source}))
def check(name,condition):
    results.append({'prueba':name,'resultado':'OK' if condition else 'ERROR'})
    print(('OK ' if condition else 'ERROR ')+name,flush=True)
    assert condition,name

def run():
    original=sql('SELECT * FROM habitaciones ORDER BY id')
    status,body=get('')
    check('READ: Apache muestra el listado',status==200 and b'Sistema de Reserva de Habitaciones' in body)
    check('Datos demo visibles',all(code.encode() in body for code in ['H101','H102','H103']))
    check('CSRF: POST sin token rechazado',post('habitaciones/guardar',{},'habitaciones/crear',False)[0]==403)
    types=[('sencilla',1,'100.00'),('doble',2,'200.00'),('triple',3,'300.00')]
    states=['disponible','mantenimiento','ocupada']; created=[]
    try:
        for i,(tipo,capacity,price) in enumerate(types):
            for j,estado in enumerate(states):
                code='TEST-'+uuid.uuid4().hex[:8]
                data={'codigo':code,'tipo':tipo,'estado':estado,'fecha':'2026-10-27','capacidad':'999','precio_noche':'9999'}
                status,body=post('habitaciones/guardar',data,'habitaciones/crear')
                hid=sql("SELECT id FROM habitaciones WHERE codigo='"+code+"'")
                if hid: created.append(hid)
                check('CREATE '+tipo+' / '+estado,status==200 and bool(hid) and code.encode() in body)
                actual=sql('SELECT tipo,capacidad,precio_noche,estado,fecha FROM habitaciones WHERE id='+hid)
                check('Regla PHP y fecha '+tipo+' / '+estado,actual==f'{tipo}\t{capacity}\t{price}\t{estado}\t2026-10-27')
                # Cambiar el tipo obliga a recalcular capacidad y precio.
                next_type,next_capacity,next_price=types[(i+1)%3]
                changed=dict(data,tipo=next_type,estado=states[(j+1)%3])
                status,body=post('habitaciones/actualizar/'+hid,changed,'habitaciones/editar/'+hid)
                check('UPDATE recalcula '+tipo+' a '+next_type,status==200 and sql('SELECT capacidad,precio_noche FROM habitaciones WHERE id='+hid)==f'{next_capacity}\t{next_price}')
        hid=created[0]; code=sql('SELECT codigo FROM habitaciones WHERE id='+hid)
        data={'codigo':code,'tipo':'doble','estado':'disponible','fecha':'2026-10-27'}
        status,body=post('habitaciones/guardar',data,'habitaciones/crear')
        check('Código duplicado rechazado con mensaje',status==200 and 'Ya existe una habitación'.encode() in body)
        for campo,valor in [('codigo',''),('codigo','   '),('codigo',' H101 '),('codigo','X'*21),('tipo','suite'),('tipo',''),('estado','otro'),('estado',''),('fecha',''),('fecha','2026-02-30')]:
            invalid=dict(data,codigo='INV-'+uuid.uuid4().hex[:8]);invalid[campo]=valor
            count=sql('SELECT COUNT(*) FROM habitaciones')
            status,body=post('habitaciones/guardar',invalid,'habitaciones/crear')
            check('Validación '+campo+' '+repr(valor),status==200 and b'role="alert"' in body and sql('SELECT COUNT(*) FROM habitaciones')==count)
        before=sql('SELECT * FROM habitaciones WHERE id='+hid)
        status,body=post('habitaciones/actualizar/'+hid,dict(data,tipo='incorrecto'),'habitaciones/editar/'+hid)
        check('UPDATE inválido conserva fila',status==200 and before==sql('SELECT * FROM habitaciones WHERE id='+hid))
        check('Registro inexistente devuelve 404',get('habitaciones/editar/99999999')[0]==404)
        check('GET no elimina',get('habitaciones/eliminar/'+hid)[0]==404 and bool(sql('SELECT id FROM habitaciones WHERE id='+hid)))
        check('Confirmación de eliminación declarada',b"confirm('" in get('habitaciones')[1])
        # No enviar precio/capacidad también es válido: el servidor los determina.
        status,body=post('habitaciones/actualizar/'+hid,data,'habitaciones/editar/'+hid)
        check('Servidor no depende de JavaScript ni campos calculados',status==200 and sql('SELECT capacidad,precio_noche FROM habitaciones WHERE id='+hid)=='2\t200.00')
        status,body=post('habitaciones/eliminar/'+hid,{},'habitaciones')
        check('DELETE: fila eliminada en MySQL y listado',status==200 and not sql('SELECT id FROM habitaciones WHERE id='+hid) and code.encode() not in body)
        check('Listado sin errores PHP visibles',b'ErrorException' not in body and b'Fatal error' not in body)
    finally:
        for hid in created:
            if sql('SELECT id FROM habitaciones WHERE id='+hid):
                post('habitaciones/eliminar/'+hid,{},'habitaciones')
    check('Datos originales conservados',sql('SELECT * FROM habitaciones ORDER BY id')==original)

if __name__=='__main__':
    try: run()
    finally: (ROOT/'writable/pruebas_crud.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
