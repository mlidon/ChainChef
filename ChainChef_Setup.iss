; ChainChef_Setup.iss
[Setup]
AppName=ChainChef
AppVersion=1.0
DefaultDirName={pf}\ChainChef
DefaultGroupName=ChainChef
OutputDir=.\installer
OutputBaseFilename=ChainChef_Installer
SetupIconFile=frontend\img\logo_dark.ico
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
; Pedir reinicio si es necesario (por la instalación de Ollama)
RestartIfNeededByRun=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
; Copiar todo el contenido de la carpeta dist\ChainChef (el ejecutable + dependencias)
Source: "dist\ChainChef\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

; Incluir script PowerShell que descargará Ollama
Source: "install_ollama.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\ChainChef"; Filename: "{app}\ChainChef.exe"; WorkingDir: "{app}"
Name: "{group}\ChainChef"; Filename: "{app}\ChainChef.exe"

[Run]
; Ejecutar el script PowerShell para verificar/instalar Ollama (oculto)
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\install_ollama.ps1"""; \
    Flags: runhidden waituntilterminated; StatusMsg: "Verificando/Instalando Ollama..."

; Iniciar ChainChef al finalizar la instalación
Filename: "{app}\ChainChef.exe"; Description: "Iniciar ChainChef"; Flags: nowait postinstall skipifsilent