# install_ollama.ps1
$ollamaUrl = "https://ollama.com/download/OllamaSetup.exe"
$installerPath = "$env:TEMP\OllamaSetup.exe"

Write-Host "Verificando si Ollama está instalado..."

# Comprobar si ollama ya está en el PATH
$ollamaExists = Get-Command ollama -ErrorAction SilentlyContinue

if ($ollamaExists) {
    Write-Host "Ollama ya está instalado. Versión: $(ollama --version)"
    exit 0
}

Write-Host "Ollama no encontrado. Descargando instalador..."
Invoke-WebRequest -Uri $ollamaUrl -OutFile $installerPath

Write-Host "Instalando Ollama silenciosamente..."
Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait

Write-Host "Ollama instalado correctamente."
# Limpiar
Remove-Item $installerPath -Force