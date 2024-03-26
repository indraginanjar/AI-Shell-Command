python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
deactivate
$Path = [System.Environment]::GetEnvironmentVariable("Path", "User")
$CurrentFolder = Get-Location
[Environment]::SetEnvironmentVariable("Path", "$Path;$CurrentFolder", "User")
