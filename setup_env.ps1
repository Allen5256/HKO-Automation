# setup_env.ps1

$ErrorActionPreference = "Stop"

# 1) Create .venv if not exists
if (Get-Command py -ErrorAction SilentlyContinue) {
    py -m venv .venv
} else {
    python -m venv .venv
}

# 2) Locate .venv python and pip
$venvPy  = ".\.venv\Scripts\python.exe"
$venvPip = ".\.venv\Scripts\pip.exe"

if (-not (Test-Path $venvPy)) {
    throw "Cannot find $venvPy. The virtual environment was not created correctly."
}
if (-not (Test-Path $venvPip)) {
    # Some environment might only contain pip3.exe
    $venvPip = ".\.venv\Scripts\pip3.exe"
    if (-not (Test-Path $venvPip)) {
        throw "Cannot find pip inside .venv. Please check your Python installation."
    }
}

# 3) Activate .venv in this shell
.\.venv\Scripts\Activate.ps1

# 4) Install/update dependencies
& $venvPy -m pip install --upgrade pip
& $venvPip install -r requirements.txt

Write-Host "Environment ready."
