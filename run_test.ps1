param(
    [string]$Target = "",
    [ValidateSet("UI", "API")] [string]$Scope = "UI",
    [switch]$OnlyOnFail
)

$ErrorActionPreference = "Stop"

function Load-EnvFile([string]$filePath) {
    if (-not (Test-Path $filePath)) { return }
    Get-Content $filePath | ForEach-Object {
        $line = $_.Trim()
        if ($line -eq "" -or $line.StartsWith("#")) { return }
        $kv = $line -split "=", 2
        if ($kv.Count -eq 2) {
            $key = $kv[0].Trim()
            $val = $kv[1].Trim()
            if ($val.StartsWith('"') -and $val.EndsWith('"')) {
                $val = $val.Trim('"')
            }
            [System.Environment]::SetEnvironmentVariable($key, $val, 'Process')
        }
    }
}

# Select venv-aware executables if present
$python = "python"
$pytest = "pytest"
if (Test-Path ".\.venv\Scripts\python.exe") {
    $python = ".\.venv\Scripts\python.exe"
    $pytest = ".\.venv\Scripts\pytest.exe"
}

# Load env files: common + scope-specific
Load-EnvFile "config\common.env"
if ($Scope -eq "UI") { Load-EnvFile "config\ui.env" }
if ($Scope -eq "API") { Load-EnvFile "config\api.env" }

# Mark scope for downstream tools if needed
$env:TEST_SCOPE = $Scope

# Allure result dir
$allureDir = "allure_results"
if (Test-Path $allureDir) { Remove-Item $allureDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $allureDir | Out-Null

# Build pytest command
$pytestArgs = @("--alluredir=$allureDir")

# Determine base path to limit to scope
$basePath = if ($Scope -eq "UI") { "tests\mobile" } else { "tests\api" }

# If a target is specified, use -k with the module stem (pytest -k)
if ($Target -ne "") {
    $pattern = [System.IO.Path]::GetFileNameWithoutExtension($Target)
    if ($null -eq $pattern -or $pattern -eq "") { $pattern = $Target }
    Write-Host "Running Scope=$Scope with -k $pattern under $basePath"
    & $pytest $basePath "-k" $pattern @pytestArgs
} else {
    Write-Host "Running full Scope=$Scope under $basePath"
    & $pytest $basePath @pytestArgs
}

$exitCode = $LASTEXITCODE

# Generate Allure report according to OnlyOnFail flag
$shouldGenerate = $true
if ($OnlyOnFail.IsPresent -and $exitCode -eq 0) {
    $shouldGenerate = $false
}

if ($shouldGenerate) {
    Write-Host "Generating Allure report..."
    $allure = "allure"
    & $allure generate $allureDir "-o" "allure_report" "--clean"
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Allure generation failed. Ensure Allure CLI is installed and on PATH."
    } else {
        Write-Host "Allure report generated at .\allure_report"
        allure serve $allureDir
    }
} else {
    Write-Host "All tests passed and -OnlyOnFail is set. Skipping Allure report generation."
}

exit $exitCode
