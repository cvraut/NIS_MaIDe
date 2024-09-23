# script to unnest potentially nested folders of nd2 files
# perhaps integrate multiple folders selection into the folder selector dialog
# but this script should be a 🩹 fix for now

param (
    [Parameter(Mandatory=$false)][string]$sourceDir = (Get-Location).Path,
    [Parameter(Mandatory=$false)][string]$destDir = (Join-Path (Get-Location).Path "unnested_nd2s"),
    [switch]$help
)

function Show-Help {
    Write-Host "Usage: .\unnest_nd2.ps1 [-sourceDir <source_directory>] [-destDir <destination_directory>] [--help]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -sourceDir   Specify the source directory containing .nd2 files (default: current directory)"
    Write-Host "  -destDir     Specify the destination directory for copied files (default: ./unnested_nd2s)"
    Write-Host "  --help       Display this help message"
    exit
}

if ($help) {
    Show-Help
}

# Ensure the destination directory exists
if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir | Out-Null
}

# get the full path name of sourceDir
$sdfp = (Get-Item $sourceDir).FullName
# if the last character of the sourceDir is not a backslash, add one
if ($sdfp[-1] -ne '\') {
    $sdfp += '\'
}

# Find all .nd2 files recursively
Get-ChildItem -Path $sourceDir -Filter *.nd2 -Recurse | ForEach-Object {
    # Get the relative path of the file (note do not add 1 here due to added backslash)
    $relativePath = $_.FullName.Substring($sdfp.Length)
    
    # print the relativePath (for debugging)
    #Write-Host $relativePath

    # Replace directory separators with underscores
    $newName = $relativePath -replace '\\', '_'
    
    # Copy the file to the destination with the new name
    Copy-Item $_.FullName -Destination (Join-Path $destDir $newName)
}

Write-Host "nd2 unnesting complete."
