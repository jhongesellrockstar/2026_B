"""Constructor externo de Callao Limpio. Python 3.12, Windows, VS Code."""
from __future__ import annotations
import argparse
import collections
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import queue
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen
from urllib.parse import urlparse, parse_qs

from build_plan import (REFERENCE, TARGET, FILES, AUXILIARIES, SPEEDS,
                        make_plan, source_bytes, simulate, verificar_resultado)

TOOL_DIR = Path(__file__).resolve().parent
RUNTIME = TOOL_DIR / '.runtime'
NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
BRIDGE_TIMEOUT = float(os.environ.get('PW2_BRIDGE_TIMEOUT', '30'))
EXTENSION_JS = r"""
const vscode = require('vscode');
const http = require('http');
const fs = require('fs');
const path = require('path');
const sessionFile = JSON.parse(fs.readFileSync(path.join(__dirname, 'session-path.json'), 'utf8'));
const cfg = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
const sleep = ms => new Promise(r => setTimeout(r, ms));
let dead = false, control = {paused:false, abort:false, stopped:false}, lastControl = 0;
let activeJob=null, eventSerial=0;
async function event(phase, message){
  if(activeJob)await api('/event',{id:activeJob.id+'-'+phase+'-'+(++eventSerial),operation_id:activeJob.id,phase,message});
}
const terminals = new Set();
function assertFront(){
  if(!vscode.window.state.focused)throw Error('VS Code no está al frente; vuelva a enfocarlo y reintente');
}
function assertEditor(doc){
  assertFront();
  if(vscode.window.activeTextEditor?.document.uri.toString()!==doc.uri.toString())
    throw Error('Cambió la pestaña activa; se detuvo la edición');
}
async function focusGuard(doc){
  // Allow the pause button's click to reach the controller, without editing while unfocused.
  const deadline=Date.now()+500;
  while(!vscode.window.state.focused){
    await gate();
    if(vscode.window.state.focused)break;
    if(Date.now()>deadline)assertFront();
    await sleep(25);
  }
  if(doc)assertEditor(doc);else assertFront();
}
async function visibleWait(ms, doc){
  for(let elapsed=0;elapsed<ms;elapsed+=25){
    await gate(); await focusGuard(doc); await sleep(25);
  }
}
async function reveal(doc, offset=0, restoring=false){
  assertFront();
  await vscode.commands.executeCommand('workbench.action.closePanel');
  const editor=await vscode.window.showTextDocument(doc,{
    preview:false,preserveFocus:false,viewColumn:vscode.ViewColumn.One});
  await vscode.commands.executeCommand('workbench.action.focusActiveEditorGroup');
  const caret=doc.positionAt(offset);
  editor.selection=new vscode.Selection(caret,caret);
  editor.revealRange(new vscode.Range(caret,caret),vscode.TextEditorRevealType.InCenterIfOutsideViewport);
  if(restoring){await sleep(100);assertEditor(doc);}else{await visibleWait(400,doc);}
  await event('reveal','Archivo activo y visible');
  return editor;
}
async function httpReady(url){
  return new Promise(resolve=>{
    const req=http.get(url,res=>{res.resume();resolve(res.statusCode===200);});
    req.setTimeout(500,()=>req.destroy());req.on('error',()=>resolve(false));
  });
}
async function terminalCommand(job){
  if(!job.id)throw Error('COMMAND sin identificador');
  assertFront();await gate();
  const terminal=vscode.window.createTerminal({name:job.title||'Callao Limpio',
    cwd:cfg.target,env:{npm_config_yes:'true',CI:'1'}});
  terminals.add(terminal);terminal.show(false);
  await vscode.commands.executeCommand('workbench.action.terminal.focus');
  await event('terminal','Terminal abierta');
  let subscription, execution, done=false, exitCode;
  try{
    const deadline=Date.now()+15000;
    while(!terminal.shellIntegration){
      await gate();assertFront();
      if(Date.now()>deadline)throw Error('Terminal sin integración de shell. Revise PowerShell y reintente.');
      await sleep(50);
    }
    await visibleWait(400);
    subscription=vscode.window.onDidEndTerminalShellExecution(e=>{
      if(e.execution===execution){done=true;exitCode=e.exitCode;}
    });
    const marker='__PW2_STEP_';
    const ok=marker+'OK_'+job.id+'__', bad=marker+'ERROR_'+job.id+'__';
    // Capture native exit code and PowerShell errors; printing a prompt is not an acknowledgment.
    const wrapped=job.readyUrl?job.command:
      "& { $pw2Exit=0; $global:LASTEXITCODE=0; try { & { "+job.command+
      " }; if (!$?) { $pw2Exit=1 } elseif ($LASTEXITCODE -ne 0) { $pw2Exit=$LASTEXITCODE } } "+
      "catch { Write-Host $_; $pw2Exit=1 }; if ($pw2Exit -eq 0) { Write-Output '"+ok+
      "' } else { Write-Output '"+bad+"' } }";
    execution=terminal.shellIntegration.executeCommand(wrapped);
    await event('sent','Comando enviado');
    let markerResult=null, output='';
    const reader=(async()=>{
      for await(const chunk of execution.read()){
        output=(output+chunk).slice(-16384);
        // Strip terminal escape sequences before matching standalone output lines.
        const clean=output.replace(/\x1b\][^\x07]*(?:\x07|\x1b\\)/g,'')
          .replace(/\x1b\[[0-?]*[ -/]*[@-~]/g,'');
        for(const line of clean.split(/[\r\n]+/)){
          if(line.trim()===ok)markerResult=0;
          if(line.trim()===bad)markerResult=1;
        }
      }
    })().catch(()=>{});
    const started=Date.now();
    while(markerResult===null){
      if(control.abort||control.stopped||(control.cancelled||[]).includes(activeJob?.id))throw Error('ABORTADO');
      if(!control.paused)assertFront();
      if(Date.now()-lastControl>2000)throw Error('Se perdió el controlador de terminal');
      if(job.readyUrl && !control.paused && await httpReady(job.readyUrl)){
        await event('command-finished','Servidor disponible por HTTP');
        await visibleWait(1500);return;
      }
      if(job.readyUrl && done)throw Error('El servidor terminó antes de estar disponible');
      if(done && exitCode!==0 && exitCode!==undefined)throw Error('Comando falló: '+exitCode);
      if(Date.now()-started>(job.readyUrl?30000:900000))throw Error('Comando sin completar dentro del tiempo permitido');
      await sleep(100);
    }
    await event('command-finished','Comando terminó; marcador recibido');
    if(markerResult!==0)throw Error('Comando terminó con marcador ERROR. Revise la terminal.');
    await visibleWait(1500);
    await event('confirming','Esperando confirmación');
  }catch(e){
    if(execution && !done){terminal.sendText('\x03',false);}
    throw e;
  }finally{subscription?.dispose();}
}
function api(route, payload) {
  return new Promise((resolve,reject) => {
    const req=http.request({hostname:'127.0.0.1',port:cfg.port,path:route,
      method:payload===undefined?'GET':'POST',
      headers:{Authorization:'Bearer '+cfg.token,'Content-Type':'application/json'}}, res=>{
      let body='';res.on('data',d=>body+=d);res.on('end',()=>{
        try {if(res.statusCode!==200)throw Error('HTTP '+res.statusCode);resolve(JSON.parse(body));}
        catch(e){reject(e);}
      });
    });
    req.setTimeout(2000,()=>req.destroy(Error('Sin respuesta del controlador')));
    req.on('error',reject);if(payload!==undefined)req.write(JSON.stringify(payload));req.end();
  });
}
function safeFile(rel) {
  if(!cfg.files.includes(rel))throw Error('Archivo no autorizado');
  const dest=path.resolve(cfg.target,rel);
  if(!dest.toLowerCase().startsWith(path.resolve(cfg.target).toLowerCase()+path.sep))
    throw Error('Ruta fuera del destino');
  let current=dest;
  while(current.length>=cfg.target.length){
    if(fs.existsSync(current) && fs.lstatSync(current).isSymbolicLink())throw Error('Enlace no permitido');
    const parent=path.dirname(current);if(parent===current)break;current=parent;
  }
  return dest;
}
function normalized(s){return s.replace(/\r\n/g,'\n');}
function allRange(doc){return new vscode.Range(doc.positionAt(0),doc.positionAt(doc.getText().length));}
async function replace(doc, text){
  const edit=new vscode.WorkspaceEdit();edit.replace(doc.uri,allRange(doc),text);
  if(!await vscode.workspace.applyEdit(edit))throw Error('VS Code rechazó la edición');
}
async function gate(){
  if(Date.now()-lastControl>2000)throw Error('Se perdió el control de pausa/aborto');
  if(control.abort || control.stopped || (control.cancelled||[]).includes(activeJob?.id))throw Error('ABORTADO');
  while(control.paused){await sleep(15);
    if(Date.now()-lastControl>2000)throw Error('Se perdió el controlador');
    if(control.abort || control.stopped || (control.cancelled||[]).includes(activeJob?.id))throw Error('ABORTADO');
  }
}
async function execute(job){
  if(!job?.id){await api('/protocol-error',{id:'pw2-protocol-error',message:'Operación sin id'}).catch(()=>{});return;}
  activeJob=job;
  let doc, original, edited=false;
  try {
    if(job.kind==='TERMINAL'){
      await terminalCommand(job);await api('/done',{id:job.id,status:'OK'});return;
    }
    const dest=safeFile(job.file);
    if(!fs.existsSync(dest)){
      const relative=job.file.replace(/'/g,"''");
      await terminalCommand({id:job.id+'-create',title:'Crear '+path.basename(dest),
        command:"New-Item -ItemType File -Path '"+relative+"' -ErrorAction Stop"});
    }
    doc=await vscode.workspace.openTextDocument(vscode.Uri.file(dest));
    if(doc.isDirty)throw Error('Hay cambios manuales sin guardar. Guardarlos o deshacerlos antes de F6.');
    original=doc.getText();
    if(normalized(original)!==job.before)throw Error('El archivo cambió fuera del constructor');
    const editor=await reveal(doc,job.replace?0:job.offset);
    await gate();
    assertEditor(doc);
    let expected=original;
    // A replacement starts from an empty buffer; append/insertion keeps prior code.
    if(job.replace){await replace(doc,'');edited=true;expected='';}
    let position=job.replace?0:doc.offsetAt(doc.positionAt(job.offset));
    // All controlled documents use LF during construction; final verification preserves source bytes.
    if(doc.eol!==vscode.EndOfLine.LF){
      const e=new vscode.WorkspaceEdit();e.set(doc.uri,[vscode.TextEdit.setEndOfLine(vscode.EndOfLine.LF)]);
      await vscode.workspace.applyEdit(e);expected=normalized(expected);position=job.replace?0:job.offset;
    }
    const chunks=job.mode==='TYPE'?Array.from(job.content):[job.content];
    for(const ch of chunks){
      await gate();
      await focusGuard(doc);
      if(doc.isClosed || doc.getText()!==expected)throw Error('Edición manual detectada; detener y revisar');
      const edit=new vscode.WorkspaceEdit();edit.insert(doc.uri,doc.positionAt(position),ch);
      if(!await vscode.workspace.applyEdit(edit))throw Error('No se pudo insertar');
      edited=true;expected=expected.slice(0,position)+ch+expected.slice(position);position+=ch.length;
      const caret=doc.positionAt(position);editor.selection=new vscode.Selection(caret,caret);
      editor.revealRange(new vscode.Range(caret,caret),vscode.TextEditorRevealType.Default);
      if(job.mode==='TYPE')await sleep(job.interval*1000);
    }
    await gate();
    assertEditor(doc);
    if(job.mode==='INSERT'){
      const begin=job.replace?0:job.offset;
      editor.selection=new vscode.Selection(doc.positionAt(begin),doc.positionAt(position));
      editor.revealRange(new vscode.Range(doc.positionAt(begin),doc.positionAt(position)),
        vscode.TextEditorRevealType.InCenterIfOutsideViewport);
      await visibleWait(1500,doc);
    }
    if(normalized(doc.getText())!==job.after)throw Error('Contenido inesperado al terminar');
    const finalEol=job.crlf?vscode.EndOfLine.CRLF:vscode.EndOfLine.LF;
    if(doc.eol!==finalEol){
      const e=new vscode.WorkspaceEdit();e.set(doc.uri,[vscode.TextEdit.setEndOfLine(finalEol)]);
      if(!await vscode.workspace.applyEdit(e))throw Error('No se pudo conservar el fin de línea');
    }
    if(job.save && !await doc.save())throw Error('No se pudo guardar');
    await event('save','Archivo guardado');
    assertEditor(doc);
    await api('/done',{id:job.id,status:'OK'});
  } catch(e) {
    let rollback=true;
    if(doc && original!==undefined && edited){
      try{
        // Never roll back invisibly in a different tab/window.
        await reveal(doc,0,true);assertEditor(doc);
        await replace(doc,original);if(!await doc.save())throw Error('save');
      }
      catch(_){rollback=false;}
    }
    await api('/done',{id:job.id,status:String(e.message)==='ABORTADO'&&rollback?'ABORTADO':'ERROR',
      error:String(e.message)+(rollback?'':' (no se pudo restaurar el bloque; revise el archivo)')}).catch(()=>{});
  } finally {activeJob=null;}
}
exports.activate=async context=>{
  const folders=vscode.workspace.workspaceFolders||[];
  if(folders.length!==1 || path.resolve(folders[0].uri.fsPath).toLowerCase()!==path.resolve(cfg.target).toLowerCase())
    return;
  await vscode.commands.executeCommand('workbench.view.explorer');
  const status=vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left);
  status.text='Callao Limpio · F6 siguiente · F7 pausar/reanudar · F8 finalizar';status.show();context.subscriptions.push(status);
  context.subscriptions.push({dispose(){dead=true;}});
  const pollControl=async()=>{
    if(dead)return;
    try{control=await api('/control');lastControl=Date.now();}
    catch(_){/* Health alone does not stop the application. Active jobs have bounded waits. */}
    if(control.stopped){for(const t of terminals)t.dispose();terminals.clear();}
    if(!dead)setTimeout(pollControl,100);
  };
  pollControl();
  await api('/hello',{id:'pw2-hello',ready:true});
  while(!dead){
    try{
      const job=await api('/next');
      if(job){await execute(job);}else{await sleep(75);}
    }catch(_){await sleep(250);}
  }
};
exports.deactivate=()=>{dead=true;};
"""


class Aborted(Exception):
    pass


class SynchronizationError(Exception):
    pass


def guarded_path(target: Path, relative: str) -> Path:
    if relative not in FILES and relative not in AUXILIARIES:
        raise ValueError('Ruta no autorizada: '+relative)
    dest = target / relative
    if not dest.resolve().is_relative_to(target.resolve()):
        raise ValueError('La ruta sale de la carpeta objetivo')
    for p in [target, *dest.parents, dest]:
        if p == target or p.is_relative_to(target):
            if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
                raise ValueError('No se permiten enlaces ni junctions en el destino')
    return dest


def npm_command(*args):
    npm = shutil.which('npm')
    node = shutil.which('node')
    if not npm or not node:
        raise RuntimeError('Falta Node/npm en PATH. Instalar Node antes del ensayo.')
    cli = Path(npm).parent / 'node_modules/npm/bin/npm-cli.js'
    if not cli.is_file():
        raise RuntimeError('No se encontró npm-cli.js junto a npm: '+str(cli))
    return [node, str(cli), *args]


def code_executable():
    cmd = shutil.which('code')
    if cmd:
        exe = Path(cmd).resolve().parent.parent / 'Code.exe'
        if exe.is_file():
            return str(exe)
    exe = Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/Microsoft VS Code/Code.exe'
    if exe.is_file():
        return str(exe)
    raise RuntimeError('No se encontró VS Code. Debe estar instalado y tener el comando code.')


def ps_quote(value):
    return "'"+str(value).replace("'", "''")+"'"


class Bridge:
    """Buzón local autenticado; solo se permiten documentos del plan."""
    def __init__(self, engine, runtime):
        self.engine, self.runtime = engine, runtime
        self.token = secrets.token_urlsafe(32)
        self.ready = threading.Event()
        self.pending = queue.Queue()
        self.results = {}
        self.jobs = {}
        self.cancelled = set()
        self.last_request_id = None
        self.waiting_command_since = None
        self.condition = threading.Condition()
        self.last_seen = 0
        bridge = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def answer(self, data, status=200):
                body = json.dumps(data).encode()
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                try:
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def authorized(self):
                return self.headers.get('Authorization') == 'Bearer '+bridge.token

            def do_GET(self):
                if not self.authorized():
                    return self.answer({}, 403)
                if self.path == '/control':
                    bridge.last_seen = time.monotonic()
                    bridge.ready.set()
                    return self.answer({'paused':engine.paused.is_set(),
                                        'abort':engine.abort.is_set(), 'stopped':engine.stopped.is_set(),
                                        'cancelled':list(bridge.cancelled)})
                if self.path == '/next':
                    try:
                        job = bridge.pending.get_nowait()
                    except queue.Empty:
                        job = None
                    if job and job['id'] in bridge.cancelled:
                        job = None
                    return self.answer(job)
                if self.path == '/health':
                    return self.answer({'ok':True})
                self.answer({}, 404)

            def do_POST(self):
                if not self.authorized():
                    return self.answer({}, 403)
                try:
                    size = int(self.headers.get('Content-Length', 0))
                    if not 0 <= size <= 100000:
                        return self.answer({'error':'payload demasiado grande'}, 413)
                    self.connection.settimeout(5)
                    body = json.loads(self.rfile.read(size) or b'{}')
                except (ValueError, UnicodeError, OSError):
                    engine.log('ERROR bridge: JSON inválido')
                    return self.answer({'error':'JSON inválido'},400)
                if not isinstance(body,dict):
                    return self.answer({'error':'Se esperaba un objeto JSON'},400)
                request_id = body.get('id')
                if not isinstance(request_id,str) or not request_id.strip() or len(request_id)>200:
                    engine.log('Bridge recibió mensaje sin id')
                    engine.log('ADVERTENCIA bridge: respuesta sin id ignorada; servidor activo')
                    engine.technical('POST sin id: '+repr(body))
                    return self.answer({'error':'Bridge recibió mensaje sin id'},400)
                if self.path == '/hello':
                    bridge.ready.set()
                    bridge.last_seen=time.monotonic()
                elif self.path == '/done':
                    with bridge.condition:
                        if request_id not in bridge.jobs:
                            engine.log('ERROR bridge: confirmación con id desconocida')
                            return self.answer({'error':'id desconocida'},409)
                        if request_id in bridge.cancelled:
                            return self.answer({'ok':True,'ignored':'operación cancelada'})
                        if body.get('status') not in ('OK','ERROR','ABORTADO'):
                            return self.answer({'error':'status inválido'},400)
                        previous=bridge.results.get(request_id)
                        if previous and previous.get('status')!=body.get('status'):
                            return self.answer({'error':'resultado contradictorio'},409)
                        bridge.results[request_id] = body
                        bridge.condition.notify_all()
                    engine.log('Confirmación recibida: '+request_id)
                elif self.path == '/event':
                    root_id=body.get('operation_id')
                    if not isinstance(root_id,str) or root_id not in bridge.jobs:
                        return self.answer({'error':'operación desconocida'},409)
                    message=body.get('message','')
                    if isinstance(message,str):
                        engine.log(message[:200])
                elif self.path == '/protocol-error':
                    engine.log('ERROR bridge: operación recibida sin id')
                else:
                    return self.answer({}, 404)
                self.answer({'ok':True})

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def launch(self):
        extension = self.runtime / 'bridge-extension'
        profile = TOOL_DIR / '.vscode-profile'
        userdir = profile / 'user'
        extensions = profile / 'extensions'
        extension.mkdir(parents=True, exist_ok=True)
        extensions.mkdir(parents=True, exist_ok=True)
        (userdir / 'User').mkdir(parents=True, exist_ok=True)
        settings = {
            'workbench.startupEditor':'none', 'window.restoreWindows':'none',
            'workbench.welcomePage.experimentalOnboarding':False,
            'workbench.secondarySideBar.defaultVisibility':'hidden',
            'editor.formatOnSave':False, 'editor.formatOnPaste':False,
            'editor.autoIndent':'none', 'editor.autoClosingBrackets':'never',
            'editor.autoClosingQuotes':'never', 'files.autoSave':'off',
            'files.trimTrailingWhitespace':False, 'files.insertFinalNewline':False,
            'editor.minimap.enabled':False, 'editor.fontSize':17,
            'editor.wordWrap':'on', 'editor.quickSuggestions':False,
            'workbench.editor.enablePreview':False,
            'git.enabled':False,
            'window.title':'${dirty}${activeEditorShort}${separator}${rootName}${separator}Callao Limpio',
            'terminal.integrated.defaultProfile.windows':'PowerShell',
            'terminal.integrated.profiles.windows':{
                'PowerShell':{'path':str(Path(os.environ['SystemRoot'])/'System32/WindowsPowerShell/v1.0/powershell.exe'),
                              'args':['-NoLogo']}},
            'terminal.integrated.shellIntegration.enabled':True
        }
        settings_file = userdir/'User/settings.json'
        existing = json.loads(settings_file.read_text(encoding='utf-8')) if settings_file.exists() else {}
        existing.update(settings)
        settings_file.write_text(json.dumps(existing, indent=2), encoding='utf-8')
        (extension/'package.json').write_text(json.dumps({
            'name':'callao-builder-local','displayName':'Callao Builder Local',
            'publisher':'callao-local','version':'1.0.0',
            'engines':{'vscode':'^1.93.0'},'main':'./extension.js',
            'activationEvents':['onStartupFinished'],
            'capabilities':{'untrustedWorkspaces':{'supported':True}}}), encoding='utf-8')
        (extension/'extension.js').write_text(EXTENSION_JS, encoding='utf-8')
        (extension/'session-path.json').write_text(json.dumps(str(self.runtime/'connection.json')), encoding='utf-8')
        (self.runtime/'connection.json').write_text(json.dumps({
            'port':self.server.server_port,'token':self.token,
            'target':str(self.engine.target),'files':list(FILES)}), encoding='utf-8')
        # Install this local bridge in the isolated profile, not in the user's normal profile.
        vsix = self.runtime/'callao-builder-local.vsix'
        manifest = '''<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
<Metadata><Identity Language="en-US" Id="callao-builder-local" Version="1.0.0" Publisher="callao-local"/>
<DisplayName>Callao Builder Local</DisplayName><Description xml:space="preserve">Puente local de grabación</Description>
<Tags>local</Tags><Categories>Other</Categories><GalleryFlags>Public</GalleryFlags>
<Properties><Property Id="Microsoft.VisualStudio.Code.Engine" Value="^1.93.0"/>
<Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="workspace"/></Properties></Metadata>
<Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation><Dependencies/>
<Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/>
</Assets></PackageManifest>'''
        content_types = '''<?xml version="1.0"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="json" ContentType="application/json"/><Default Extension="js" ContentType="application/javascript"/>
<Default Extension="vsixmanifest" ContentType="text/xml"/></Types>'''
        with zipfile.ZipFile(vsix,'w',zipfile.ZIP_DEFLATED) as package:
            package.writestr('extension.vsixmanifest',manifest)
            package.writestr('[Content_Types].xml',content_types)
            for name in ('package.json','extension.js','session-path.json'):
                package.write(extension/name,'extension/'+name)
        exe=Path(code_executable())
        candidates=[exe.parent/'resources/app/out/cli.js', *exe.parent.glob('*/resources/app/out/cli.js')]
        cli=next((p for p in candidates if p.is_file()),None)
        if cli is None:
            raise RuntimeError('No se encontró la CLI de VS Code para instalar el puente local')
        install=subprocess.run([str(exe),str(cli),'--user-data-dir',str(userdir),
            '--extensions-dir',str(extensions),'--install-extension',str(vsix),'--force'],
            env={**os.environ,'ELECTRON_RUN_AS_NODE':'1'},stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
            creationflags=NO_WINDOW,timeout=60)
        if install.returncode:
            raise RuntimeError('No se instaló el puente local: '+install.stdout.decode(errors='replace')[-300:])
        # One ordinary VS Code window; no Extension Development Host.
        args = [str(exe), '--reuse-window', '--user-data-dir', str(userdir),
                '--extensions-dir', str(extensions), str(self.engine.target)]
        self.engine.log('Abrir VS Code: '+subprocess.list2cmdline(args))
        subprocess.Popen(args, creationflags=NO_WINDOW)
        deadline = time.monotonic()+60
        while not self.ready.wait(0.05):
            self.engine.gate()
            if time.monotonic()>deadline:
                raise RuntimeError('VS Code no conectó en 60 s. Cierre esta sesión y revise el registro.')
        self.bring_to_front()

    def bring_to_front(self):
        """Restore only this project's window, and verify foreground before any job."""
        user32=ctypes.WinDLL('user32',use_last_error=True)
        user32.GetForegroundWindow.restype=wintypes.HWND
        user32.GetWindowThreadProcessId.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.DWORD)]
        user32.GetWindowThreadProcessId.restype=wintypes.DWORD
        user32.SetForegroundWindow.argtypes=[wintypes.HWND]
        user32.ShowWindow.argtypes=[wintypes.HWND,ctypes.c_int]
        user32.GetWindowTextW.argtypes=[wintypes.HWND,wintypes.LPWSTR,ctypes.c_int]
        user32.IsWindowVisible.argtypes=[wintypes.HWND]
        matches=[]
        callback_type=ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
        @callback_type
        def collect(hwnd, _):
            title=ctypes.create_unicode_buffer(2048)
            user32.GetWindowTextW(hwnd,title,len(title))
            if user32.IsWindowVisible(hwnd) and self.engine.target.name in title.value and 'Callao Limpio' in title.value:
                matches.append(hwnd)
            return True
        user32.EnumWindows(collect,0)
        if len(matches)!=1:
            raise RuntimeError('No se encontró una única ventana de VS Code del destino. Cierre ventanas duplicadas y reintente.')
        hwnd=matches[0]
        user32.ShowWindow(hwnd,9)
        current=ctypes.windll.kernel32.GetCurrentThreadId()
        foreground=user32.GetWindowThreadProcessId(user32.GetForegroundWindow(),None)
        attached=False
        try:
            if foreground and foreground!=current:
                attached=bool(user32.AttachThreadInput(current,foreground,True))
            user32.SetForegroundWindow(hwnd)
        finally:
            if attached:user32.AttachThreadInput(current,foreground,False)
        deadline=time.monotonic()+2
        while user32.GetForegroundWindow()!=hwnd:
            if time.monotonic()>deadline:
                raise RuntimeError('Windows no permitió enfocar VS Code. Haga clic en su ventana y pulse Reintentar paso.')
            time.sleep(.025)

    def edit(self, job):
        self.engine.gate()
        self.bring_to_front()
        self.engine.log('VS Code enfocado')
        kind='command' if job.get('kind')=='TERMINAL' else job.get('mode','edit').lower()
        job['id'] = f'pw2-step-{self.engine.index+1:03d}-{kind}-{secrets.token_hex(6)}'
        self.jobs[job['id']]=job
        self.last_request_id=job['id']
        self.pending.put(job)
        self.wait_result(job['id'])

    def confirmation_timeout(self, job):
        if job.get('kind') == 'TERMINAL':
            # Include shell startup and final acknowledgment beyond the JS deadline.
            return 60 if job.get('readyUrl') else 930
        duration = len(job.get('content', '')) * job.get('interval', 0) if job.get('mode') == 'TYPE' else 0
        return max(self.engine.confirmation_timeout, duration + 30)

    def wait_result(self, request_id):
        """Wait only; never requeue or execute the operation when confirming again."""
        job = self.jobs[request_id]
        timeout = job.setdefault('confirmation_timeout', self.confirmation_timeout(job))
        started = time.monotonic()
        deadline = started + timeout
        self.waiting_command_since = started if job.get('kind') == 'TERMINAL' else None
        try:
            with self.condition:
                while request_id not in self.results:
                    self.condition.wait(0.05)
                    if self.engine.stopped.is_set() or self.engine.abort.is_set():
                        self.cancelled.add(request_id)
                        raise Aborted('Paso abortado; índice conservado.')
                    if request_id not in self.results and time.monotonic() >= deadline:
                        raise SynchronizationError('No se recibió confirmación del puente.')
                result = self.results[request_id]
            if result['status'] == 'ABORTADO':
                raise Aborted('Paso abortado; pulse Reintentar paso cuando esté preparado.')
            if result['status'] != 'OK':
                raise RuntimeError(result.get('error','Error de VS Code'))
        finally:
            self.waiting_command_since = None


class Engine:
    def __init__(self, target=TARGET, sandbox=False, emit=None):
        self.target = target.resolve()
        self.sandbox = sandbox
        if not sandbox and self.target != TARGET.resolve():
            raise ValueError('Solo se permite proyecto_tutorial en modo normal')
        if sandbox:
            temp = Path(tempfile.gettempdir()).resolve()
            if not self.target.is_relative_to(temp) or not self.target.name.startswith('pw2-builder-'):
                raise ValueError('Un ensayo debe estar en TEMP/pw2-builder-*')
        if self.target == REFERENCE.resolve() or self.target.is_relative_to(REFERENCE.resolve()):
            raise ValueError('La referencia es de solo lectura')
        if self.target.is_symlink() or self.target.is_junction():
            raise ValueError('Destino enlazado no permitido')
        if self.target.exists() and any(self.target.iterdir()):
            raise ValueError('El destino debe estar vacío. No se borra ni reemplaza una construcción anterior.')
        self.steps = make_plan()
        self.sources = source_bytes()
        self.source_hashes = {p:hashlib.sha256(b).hexdigest() for p,b in self.sources.items()}
        self.expected = {}
        self.index = 0
        self.lock = threading.Lock()
        self.busy = False
        self.paused, self.stopped, self.abort = threading.Event(), threading.Event(), threading.Event()
        self.started = None
        self.demo_started = None
        self.interval = .010
        self.status = 'LISTO'
        self.emit = emit or (lambda msg: None)
        self.runtime = RUNTIME / (time.strftime('%Y%m%d-%H%M%S')+'-'+secrets.token_hex(3))
        self.runtime.mkdir(parents=True, exist_ok=True)
        self.process = None
        self.dev_process = None
        self.bridge = None
        self.url = ''
        self.fatal = False
        self.last_completed = None
        self.error = ''
        self.confirmation_timeout = max(1,BRIDGE_TIMEOUT)
        self.sync_request = None
        self.last_activity = time.strftime('%H:%M:%S')

    def log(self, message):
        self.last_activity=time.strftime('%H:%M:%S')
        self.emit(self.last_activity+' '+message)
        with (self.runtime/'registro.log').open('a', encoding='utf-8') as f:
            f.write(time.strftime('%H:%M:%S')+' '+message+'\n')

    def technical(self, message):
        with (self.runtime/'tecnico.log').open('a',encoding='utf-8') as f:
            f.write(time.strftime('%H:%M:%S')+' '+message+'\n')

    def gate(self):
        if self.stopped.is_set() or self.abort.is_set():
            raise Aborted('Operación interrumpida.')
        while self.paused.is_set():
            if self.stopped.wait(.02) or self.abort.is_set():
                raise Aborted('Operación interrumpida.')

    def next(self):
        with self.lock:
            if self.busy or self.stopped.is_set() or self.paused.is_set() or self.fatal or self.index>=len(self.steps):
                return False
            self.busy = True
            self.abort.clear()
            self.status = 'ESCRIBIENDO' if self.steps[self.index].accion=='EDIT' else 'EJECUTANDO'
            if self.started is None:
                self.started = time.monotonic()
        threading.Thread(target=self._run, daemon=True).start()
        return True

    def pause(self):
        if self.stopped.is_set() or self.fatal:
            return
        if self.paused.is_set():
            if self.busy and self.bridge:
                try:
                    self.bridge.bring_to_front()
                except Exception as exc:
                    self.log(str(exc))
                    return
            self.paused.clear()
            self.status = ('ESCRIBIENDO' if self.steps[self.index].accion=='EDIT' else 'EJECUTANDO') if self.busy else 'LISTO'
        else:
            self.paused.set()
            self.status = 'PAUSA'
        self.log('F7: '+self.status)

    def cancel(self):
        if self.busy or self.sync_request:
            self.abort.set()
            if self.bridge and self.bridge.last_request_id:
                self.bridge.cancelled.add(self.bridge.last_request_id)
            self.sync_request=None
            self.fatal=True
            self.status = 'ABORTADO'
            self.error='Paso abortado; puede reintentar el mismo paso.'
            self.log('ESC: interrumpir bloque actual')

    def stop(self):
        self.stopped.set()
        self.abort.set()
        self.paused.clear()
        self.status = 'SESIÓN FINALIZADA'
        self.log('F8: finalizar sesión (no es una pausa)')
        for proc in (self.process, self.dev_process):
            if proc and proc.poll() is None:
                kill_tree(proc)

    def info(self):
        if self.index>=len(self.steps):
            return 'Construcción finalizada. Demostración manual: 2 minutos.'
        s = self.steps[self.index]
        completed = '' if self.busy or self.last_completed is None else f'Paso {self.last_completed} completado.\nSiguiente (espera F6):\n'
        return (completed+f'Paso {s.numero} / {len(self.steps)}\nIntegrante: {s.integrante}\n'
                f'Archivo: {s.archivo or "Terminal / proyecto"}\nAcción: {s.descripcion}\nModo: {s.modo}')

    def retry(self):
        if self.busy or self.stopped.is_set() or not self.fatal:
            return False
        if self.sync_request:
            self.log('Primero reintente la confirmación o aborte el paso; no se vuelve a enviar el comando.')
            return False
        if self.steps[self.index].accion=='START' and self.bridge is not None:
            # Reuse the existing window/bridge rather than open another window on retry.
            if not self.bridge.ready.is_set():
                self.log('La ventana no conectó. Cierre la sesión y revise el puente antes de reiniciar.')
                return False
        self.fatal=False
        self.error=''
        self.paused.clear()
        return self.next()

    def complete_step(self, number, manual=False):
        self.index=number
        self.last_completed=number
        self.sync_request=None
        self.fatal=False
        self.error=''
        self.status='SESIÓN FINALIZADA' if self.stopped.is_set() else ('PAUSA' if self.paused.is_set() else 'LISTO')
        self.log(f'Paso {number} COMPLETADO'+(' por decisión manual' if manual else ''))
        self.log('LISTO PARA F6')

    def retry_confirmation(self):
        with self.lock:
            if self.busy or not self.sync_request or self.stopped.is_set():
                return False
            self.busy=True
            self.status='ESPERANDO CONFIRMACIÓN'
        threading.Thread(target=self._confirm_only,daemon=True).start()
        return True

    def _confirm_only(self):
        try:
            request_id=self.sync_request
            self.bridge.wait_result(request_id)
            job=self.bridge.jobs[request_id]
            if job.get('file'):
                dest=guarded_path(self.target,job['file'])
                if not dest.is_file() or dest.read_text(encoding='utf-8-sig')!=job['after']:
                    raise RuntimeError('El archivo no coincide con el paso confirmado')
                self.expected[job['file']]=job['after']
            if self.steps[self.index].accion=='VERIFY' and any(v!='OK' for v in verificar_resultado(self.target).values()):
                raise RuntimeError('La verificación de archivos no pasó')
            self.complete_step(self.steps[self.index].numero)
        except SynchronizationError as exc:
            self.status='ERROR DE SINCRONIZACIÓN'
            self.error=str(exc)
            self.log(str(exc))
        except Aborted as exc:
            self.status='ABORTADO'
            self.error=str(exc)
            self.sync_request=None
        except Exception as exc:
            self.status='ERROR · '+str(exc)[:100]
            self.error=str(exc)
            self.sync_request=None
            self.log(self.status)
        finally:
            with self.lock:self.busy=False

    def mark_completed(self):
        if self.busy or not self.fatal or self.stopped.is_set():
            return False
        if self.bridge and self.bridge.last_request_id:
            self.bridge.cancelled.add(self.bridge.last_request_id)
        step=self.steps[self.index]
        if step.accion=='EDIT':
            dest=guarded_path(self.target,step.archivo)
            if dest.is_file():self.expected[step.archivo]=dest.read_text(encoding='utf-8-sig')
        self.complete_step(step.numero,manual=True)
        return True

    def _run(self):
        s = self.steps[self.index]
        try:
            self.gate()
            for p,digest in self.source_hashes.items():
                if hashlib.sha256((REFERENCE/p).read_bytes()).hexdigest()!=digest:
                    raise RuntimeError('La referencia cambió durante la sesión: '+p)
            self.log(f'PASO {s.numero} · {s.integrante} · {s.descripcion}')
            self.execute(s)
            self.complete_step(s.numero)
        except SynchronizationError as e:
            self.fatal=True
            self.sync_request=self.bridge.last_request_id
            self.error=str(e)
            self.status='ERROR DE SINCRONIZACIÓN'
            self.log(f'Paso {s.numero}: {e} Use recuperación manual; no se avanza automáticamente.')
        except Aborted as e:
            self.fatal=True
            self.error=str(e)
            self.status = 'SESIÓN FINALIZADA' if self.stopped.is_set() else 'ABORTADO · use Reintentar paso'
            self.log(str(e))
        except Exception as e:
            self.fatal = True
            self.error=str(e)
            self.status = 'SESIÓN FINALIZADA' if self.stopped.is_set() else 'ERROR · '+str(e)[:105]
            self.log(type(e).__name__+': '+str(e))
        finally:
            with self.lock:
                self.busy = False

    def command(self, command, ready_url=None):
        self.gate()
        self.log('TERMINAL VISIBLE: '+command)
        self.bridge.edit({'kind':'TERMINAL','command':command,
                          'title':'Callao Limpio · paso '+str(self.index+1),'readyUrl':ready_url})

    def execute(self, s):
        if s.accion == 'START':
            self.target.mkdir(parents=True,exist_ok=True)
            if any(self.target.iterdir()):
                raise RuntimeError('El destino dejó de estar vacío')
            if self.bridge is None:
                self.bridge = Bridge(self,self.runtime)
                self.bridge.launch()
            else:
                self.bridge.bring_to_front()
        elif s.accion == 'VITE':
            self.command('npm create vite@latest . -- --template react --no-interactive --no-immediate')
        elif s.accion == 'AUX':
            for p in AUXILIARIES:
                guarded_path(self.target,p)
            sources=','.join(ps_quote(REFERENCE/p) for p in AUXILIARIES)
            self.command("Copy-Item -LiteralPath "+sources+" -Destination . -Verbose -ErrorAction Stop")
        elif s.accion == 'INSTALL':
            self.command('npm install')
        elif s.accion == 'DIRS':
            self.command("& { $ErrorActionPreference='Stop'; "
                "New-Item -ItemType Directory -Path 'src/components','public' -Force; "
                "foreach ($logo in @('src/assets/react.svg','public/vite.svg')) { "
                "if (Test-Path -LiteralPath $logo) { Remove-Item -LiteralPath $logo -Verbose } }; "
                "Write-Host 'Plantilla limpia. main.jsx, App.jsx y CSS se reemplazan VISUALMENTE en los siguientes pasos.' }")
        elif s.accion == 'EDIT':
            dest = guarded_path(self.target,s.archivo)
            disk = dest.read_text(encoding='utf-8-sig') if dest.exists() else ''
            before = self.expected.get(s.archivo,disk)
            if disk != before:
                raise RuntimeError('Se modificó el destino fuera del constructor: '+s.archivo)
            offset = len(before) if s.offset is None else s.offset
            after = s.contenido if s.reemplazar else before[:offset]+s.contenido+before[offset:]
            self.bridge.edit({'file':s.archivo,'before':before,'after':after,
                'replace':s.reemplazar,'offset':offset,'content':s.contenido,
                'mode':s.modo,'interval':self.interval,'save':s.guardar,
                'crlf':b'\r\n' in self.sources[s.archivo]})
            if dest.read_text(encoding='utf-8-sig') != after:
                raise RuntimeError('El archivo guardado no coincide: '+s.archivo)
            self.expected[s.archivo] = after
        elif s.accion == 'VERIFY':
            paths=','.join(ps_quote(p) for p in FILES)
            self.command("& { $ErrorActionPreference='Stop'; foreach ($archivo in @("+paths+")) { "
                "$origen=Join-Path "+ps_quote(REFERENCE)+" $archivo; "
                "if (!(Test-Path -LiteralPath $archivo)) { Write-Host ('FALTA '+$archivo) } "
                "elseif ((Get-FileHash -LiteralPath $archivo).Hash -eq (Get-FileHash -LiteralPath $origen).Hash) "
                "{ Write-Host ('OK '+$archivo) } else { Write-Host ('DIFERENTE '+$archivo) } } }")
            result=verificar_resultado(self.target)
            self.log(json.dumps(result,ensure_ascii=False))
            if any(v!='OK' for v in result.values()):
                raise RuntimeError('La verificación no pasó')
        elif s.accion == 'BUILD':
            self.command('npm run build')
        elif s.accion == 'DEV':
            with socket.socket() as sock:
                sock.bind(('127.0.0.1',0))
                port=sock.getsockname()[1]
            self.url=f'http://127.0.0.1:{port}/'
            self.command(f'npm run dev -- --host 127.0.0.1 --port {port} --strictPort',self.url)
            self.log('SERVIDOR LISTO: '+self.url)
        elif s.accion == 'BROWSER':
            edge = next((p for p in [
                Path(os.environ.get('PROGRAMFILES(X86)',''))/'Microsoft/Edge/Application/msedge.exe',
                Path(os.environ.get('PROGRAMFILES',''))/'Microsoft/Edge/Application/msedge.exe'
            ] if p.is_file()),None)
            if not edge:
                raise RuntimeError('No se encontró Microsoft Edge. URL: '+self.url)
            subprocess.Popen([str(edge),'--new-window',self.url])
            self.demo_started=time.monotonic()
            self.log('Demostración manual: 2 minutos. El puerto independiente evita usar datos del original.')

    def timing(self):
        elapsed=0 if self.started is None else time.monotonic()-self.started
        construction=sum(s.integrante!='FINAL' for s in self.steps)
        ratio=min(self.index,construction)/construction
        return elapsed,ratio,ratio*28*60-elapsed


def kill_tree(proc):
    if proc.poll() is None:
        subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],
                       stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=NO_WINDOW)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass


def clock(seconds):
    seconds=max(0,int(seconds))
    return f'{seconds//60:02d}:{seconds%60:02d}'


class ControlWindow:
    def __init__(self, engine, register_hotkeys=True):
        self.engine=engine
        self.queue=queue.Queue()
        engine.emit=self.queue.put
        self.root=tk.Tk()
        self.root.title('CALLAO LIMPIO · Constructor guiado'+(' · ENSAYO TEMPORAL' if engine.sandbox else ''))
        self.root.geometry('650x880')
        self.root.minsize(620,760)
        self.root.configure(bg='#f3f6f3')
        self.root.protocol('WM_DELETE_WINDOW',self.close)
        # No topmost; all widget mutations happen only on the Tk main thread.
        style=ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame',background='#f3f6f3')
        style.configure('TLabel',background='#f3f6f3',font=('Segoe UI',10))
        panel=ttk.Frame(self.root,padding=20)
        panel.pack(fill='both',expand=True)
        ttk.Label(panel,text='CALLAO LIMPIO',font=('Segoe UI',22,'bold'),foreground='#173e35').pack(anchor='w')
        ttk.Label(panel,text='Constructor guiado · '+('ensayo temporal' if engine.sandbox else 'proyecto_tutorial')).pack(anchor='w',pady=(0,14))
        self.info=tk.StringVar()
        self.state=tk.StringVar(value='LISTO')
        self.time=tk.StringVar()
        ttk.Label(panel,textvariable=self.info,wraplength=565,justify='left').pack(fill='x',anchor='w')
        ttk.Label(panel,textvariable=self.state,wraplength=565,font=('Segoe UI',12,'bold'),foreground='#245c47').pack(anchor='w',pady=10)
        self.system=tk.StringVar()
        system_panel=ttk.LabelFrame(panel,text='ESTADO DEL SISTEMA',padding=6)
        system_panel.pack(fill='x',pady=(0,6))
        ttk.Label(system_panel,textvariable=self.system,justify='left').pack(anchor='w')
        self.progress=ttk.Progressbar(panel,maximum=len(engine.steps))
        self.progress.pack(fill='x')
        ttk.Label(panel,textvariable=self.time,justify='left').pack(anchor='w',pady=8)
        speeds=ttk.Frame(panel);speeds.pack(fill='x')
        ttk.Label(speeds,text='Segundos por carácter: ').pack(side='left')
        self.speed=tk.StringVar(value='0.010')
        box=ttk.Combobox(speeds,textvariable=self.speed,values=[f'{v:.3f}' for v in SPEEDS],state='readonly',width=8)
        box.pack(side='left')
        box.bind('<<ComboboxSelected>>',lambda _:setattr(engine,'interval',float(self.speed.get())))
        buttons=ttk.Frame(panel);buttons.pack(fill='x',pady=12)
        self.next_button=ttk.Button(buttons,text='F6 Siguiente',command=engine.next)
        self.next_button.pack(side='left',padx=2)
        self.retry_button=ttk.Button(buttons,text='Reintentar paso',command=self.retry)
        self.retry_button.pack(side='left',padx=2)
        recovery=ttk.Frame(panel);recovery.pack(fill='x',pady=(0,8))
        self.confirm_button=ttk.Button(recovery,text='REINTENTAR CONFIRMACIÓN',command=engine.retry_confirmation)
        self.confirm_button.pack(side='left',padx=2)
        self.mark_button=ttk.Button(recovery,text='MARCAR PASO COMPLETADO',command=self.mark_completed)
        self.mark_button.pack(side='left',padx=2)
        self.abort_button=ttk.Button(recovery,text='ABORTAR PASO',command=engine.cancel)
        self.abort_button.pack(side='left',padx=2)
        session_buttons=ttk.Frame(panel);session_buttons.pack(fill='x',pady=(0,10))
        ttk.Button(session_buttons,text='F7 PAUSAR / REANUDAR',command=engine.pause).pack(side='left',padx=2)
        ttk.Button(session_buttons,text='F8 FINALIZAR SESIÓN',command=engine.stop).pack(side='left',padx=2)
        ttk.Label(panel,text='F9 Información · ESC ABORTAR PASO ACTUAL\nNO usar F8 para una pausa. Atajos globales.').pack(anchor='w')
        self.logbox=tk.Text(panel,height=9,wrap='word',font=('Consolas',9),state='disabled')
        self.logbox.pack(fill='both',expand=True,pady=(12,0))
        self.hooks=[]
        import keyboard
        self.keyboard=keyboard
        # Release events avoid key-repeat; no F6 events are queued while running.
        for key,fn in ([] if not register_hotkeys else [('f6',engine.next),('f7',engine.pause),('f8',engine.stop),
                       ('f9',lambda:self.queue.put('__INFO__')),('esc',engine.cancel)]):
            self.hooks.append(keyboard.on_release_key(key,lambda event,f=fn:f(),suppress=True))
        self.closing=False
        self.refresh()
        self.heartbeat()

    def heartbeat(self):
        if self.closing:return
        e=self.engine
        connected=bool(e.bridge and time.monotonic()-e.bridge.last_seen<3)
        phase='ERROR' if e.fatal else ('PAUSADO' if e.paused.is_set() else ('EJECUTANDO' if e.busy else e.status))
        waiting = e.bridge.waiting_command_since if e.bridge else None
        wait_text = ''
        if waiting is not None and e.busy:
            if not e.paused.is_set() and not e.stopped.is_set():
                phase = 'EJECUTANDO COMANDO'
            wait_text = '\nEsperando finalización del comando npm/Vite... Tiempo de espera: '+clock(time.monotonic()-waiting)
        self.system.set('Python: ACTIVO · Último heartbeat: '+time.strftime('%H:%M:%S')+
            '\nBridge: '+('CONECTADO / OK' if connected else 'DESCONECTADO / SIN RESPUESTA')+
            ' · VS Code: '+('DISPONIBLE' if connected and e.bridge.ready.is_set() else 'NO DISPONIBLE')+
            '\nPaso: '+phase+' · Última actividad: '+e.last_activity+wait_text)
        self.root.after(1000,self.heartbeat)

    def mark_completed(self):
        if messagebox.askyesno('Recuperación manual',
            '¿Confirma que el paso ya terminó correctamente? No se ejecutará otra vez ni se validará automáticamente. '
            'Se invalidará cualquier respuesta tardía de esa operación y se avanzará solo un paso.',parent=self.root):
            self.engine.mark_completed()

    def retry(self):
        if self.engine.busy or self.engine.stopped.is_set() or not self.engine.fatal:
            return
        if messagebox.askyesno('Reintentar el mismo paso',
                self.engine.error+'\n\nRevise el archivo o la salida de terminal. '
                'Un comando interrumpido puede haber dejado cambios parciales. '
                '¿Reintentar este paso sin avanzar el índice?',parent=self.root):
            self.engine.retry()

    def refresh(self):
        while True:
            try:
                msg=self.queue.get_nowait()
            except queue.Empty:
                break
            if msg=='__INFO__':
                self.root.deiconify()
                msg='SIGUIENTE: '+self.engine.info()
            self.logbox.configure(state='normal')
            self.logbox.insert('end',msg+'\n')
            self.logbox.see('end')
            self.logbox.configure(state='disabled')
        e=self.engine
        self.info.set(e.info()+('\nDetalle: '+e.error[:180] if e.fatal else ''))
        self.state.set(e.status)
        disabled=e.busy or e.paused.is_set() or e.stopped.is_set() or e.fatal or e.index>=len(e.steps)
        self.next_button.configure(state='disabled' if disabled else 'normal')
        recover=e.fatal and not e.busy and not e.stopped.is_set()
        self.retry_button.configure(state='normal' if recover and not e.sync_request else 'disabled')
        self.confirm_button.configure(state='normal' if recover and e.sync_request else 'disabled')
        self.mark_button.configure(state='normal' if recover else 'disabled')
        self.abort_button.configure(state='normal' if (e.busy or e.sync_request) and not e.stopped.is_set() else 'disabled')
        self.progress['value']=e.index
        elapsed,ratio,delta=e.timing()
        label='ADELANTADO' if delta>=0 else 'RETRASADO'
        text=f'Tiempo: {clock(elapsed)} / 28:00 construcción\nPasos: {e.index}/{len(e.steps)} ({e.index/len(e.steps):.0%}) · Temporal: {elapsed/1680:.0%}\n{label} {clock(abs(delta))} respecto al avance por pasos'
        if e.demo_started:
            text+=f'\nDemostración: {clock(time.monotonic()-e.demo_started)} / 02:00 · Total objetivo 30:00'
        self.time.set(text)
        if not self.closing:
            self.root.after(100,self.refresh)

    def close(self):
        self.engine.stop()
        self.closing=True
        def finish():
            if self.engine.busy:
                self.root.after(100,finish)
                return
            for h in self.hooks:
                self.keyboard.unhook(h)
            if self.engine.bridge:
                threading.Thread(target=self.engine.bridge.server.shutdown,daemon=True).start()
            self.root.destroy()
        finish()

    def run(self):
        self.root.mainloop()


def self_test():
    """Sin GUI, sin hotkeys, sin npm; usa exclusivamente una carpeta temporal."""
    plan=make_plan()
    actual=simulate(plan)
    raw=source_bytes()
    assert set(actual)==set(FILES)
    for p,b in raw.items():
        assert actual[p]==b.decode('utf-8-sig').replace('\r\n','\n'),p
    with tempfile.TemporaryDirectory(prefix='pw2-builder-check-') as folder:
        target=Path(folder)
        assert set(verificar_resultado(target).values())=={'FALTA'}
        for p,b in raw.items():
            dest=target/p
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(b)
        assert set(verificar_resultado(target).values())=={'OK'}
        (target/FILES[0]).write_text('distinto',encoding='utf-8')
        assert verificar_resultado(target)[FILES[0]]=='DIFERENTE'
        try:
            guarded_path(target,'../proyecto/src/App.jsx')
        except ValueError:
            pass
        else:
            raise AssertionError('No se bloqueó una ruta fuera del destino')
    assert [s.numero for s in plan]==list(range(1,len(plan)+1))
    assert all(s.modo in ('TYPE','INSERT') for s in plan)
    print('SELF-TEST OK: plan íntegro, bytes, FALTA/DIFERENTE/OK y límites de rutas.')
    print(json.dumps(dict(collections.Counter(s.integrante for s in plan)),ensure_ascii=False))
    print('Pasos:',len(plan))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox',action='store_true',help='Ensayo en TEMP; nunca toca proyecto_tutorial')
    parser.add_argument('--self-test',action='store_true',help='Validación lógica sin GUI ni reconstrucción real')
    parser.add_argument('--plan',action='store_true',help='Listar pasos y salir sin abrir VS Code')
    parser.add_argument('--verificar',action='store_true',help='Comparar destino real sin modificarlo')
    args=parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.plan:
        for s in make_plan():
            print(f'{s.numero:02} {s.integrante:8} {s.modo:6} {s.archivo:44} {s.descripcion}')
        return
    if args.verificar:
        print(json.dumps(verificar_resultado(),ensure_ascii=False,indent=2))
        return
    if os.name!='nt':
        raise RuntimeError('Esta herramienta está preparada para Windows')
    target=Path(tempfile.mkdtemp(prefix='pw2-builder-')) if args.sandbox else TARGET
    engine=Engine(target,args.sandbox)
    print('DESTINO:',target,flush=True)
    print('REGISTRO:',engine.runtime,flush=True)
    ControlWindow(engine).run()


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        sys.exit(1)

