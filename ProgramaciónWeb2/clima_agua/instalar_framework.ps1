# Solo restaura el framework oficial. No modifica la app ni la base de datos.
$ErrorActionPreference = 'Stop'
if (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'system\Boot.php')) {
    Write-Host 'CodeIgniter ya está instalado.'
    exit 0
}
$temporalClima = Join-Path ([System.IO.Path]::GetTempPath()) ('clima_ci_' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $temporalClima | Out-Null
$archivoClima = Join-Path $temporalClima 'framework.zip'
Invoke-WebRequest 'https://github.com/codeigniter4/CodeIgniter4/archive/refs/tags/v4.7.5.zip' -OutFile $archivoClima
Expand-Archive -LiteralPath $archivoClima -DestinationPath $temporalClima
Copy-Item -LiteralPath (Join-Path $temporalClima 'CodeIgniter4-4.7.5\system') -Destination $PSScriptRoot -Recurse
Write-Host 'CodeIgniter 4.7.5 instalado. Continúa con README.md.'
