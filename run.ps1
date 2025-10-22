param(
    [string]$target = ""
)

$allureDir = "allure_results"
$pytestArgs = "--alluredir=$allureDir"

if ($target -eq "") {
    pytest $pytestArgs
} else {
    Write-Host "Target: $target"
    pytest -k "$target" $pytestArgs
}
