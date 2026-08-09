# setup-repo.ps1
# Creates the initial directory structure for the
# Hölderlin Psychiatry Companion repository.

$folders = @(
    "data",
    "analysis",
    "figures",
    "tables",
    "docs",
    "paper"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "Created: $folder"
    }
    else {
        Write-Host "Already exists: $folder"
    }

    # Git does not track empty directories, so add a placeholder.
    $gitkeep = Join-Path $folder ".gitkeep"

    if (-not (Test-Path $gitkeep)) {
        New-Item -ItemType File -Path $gitkeep | Out-Null
    }
}

Write-Host ""
Write-Host "Repository structure ready."