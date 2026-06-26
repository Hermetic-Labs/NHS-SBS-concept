param(
    [string]$TargetFile
)

Write-Host "Signing $TargetFile with Azure Trusted Signing (haltsigning)..."

# This uses the modern 'sign' CLI tool.
# If you use the older signtool.exe with the Azure.CodeSigning.Dlib.dll, replace the command below.
$command = "sign code trusted-signing -tse https://eus.codesigning.azure.net/ -tsa haltsigning -tscp HaltSigningProfile `"$TargetFile`""

Write-Host "Executing: $command"
Invoke-Expression $command

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to sign $TargetFile"
    exit $LASTEXITCODE
}

Write-Host "Successfully signed $TargetFile"
