[CmdletBinding()]
param (
    [Parameter(Mandatory = $true, Position = 1)]
    [ValidateNotNullOrEmpty()]
    [String] $ScriptDirectory
)

$venvActivationScriptFile = Join-Path -Path $ScriptDirectory -ChildPath \.venv\Scripts\Activate.ps1
$originalPrompt = $Prompt
. $venvActivationScriptFile
$Prompt = $originalPrompt
