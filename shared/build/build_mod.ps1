[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $ModPath,

    [ValidatePattern('^\d+\.\d+$')]
    [string] $GameVersion = '1.6',

    [string] $Configuration = 'Release'
)

$ErrorActionPreference = 'Stop'

$resolvedMod = (Resolve-Path -LiteralPath $ModPath).Path
$versionDir = Join-Path $resolvedMod $GameVersion
if (-not (Test-Path -LiteralPath $versionDir -PathType Container)) {
    throw "Version directory not found: $versionDir"
}

$projects = @(Get-ChildItem -LiteralPath $versionDir -Filter '*.csproj' -Recurse -File)
if ($projects.Count -eq 0) {
    Write-Host "No csproj found under $versionDir; treating this as an XML-only mod."
    exit 0
}

foreach ($project in $projects) {
    Write-Host "Building $($project.FullName) for RimWorld $GameVersion"
    & dotnet build $project.FullName -c $Configuration "-p:GameVersion=$GameVersion"
    if ($LASTEXITCODE -ne 0) {
        throw "dotnet build failed for $($project.FullName)"
    }
}
