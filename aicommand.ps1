<#
.SYNOPSIS
    Powershell/pwsh aicommand
.DESCRIPTION
    Powershell script for running aicommand.py
.PARAMETER Executor
    Application/executor for executing the generated command (e.g. powershell, bash) 
.PARAMETER Provider
    AI provider (openai or lmstudio). 
.PARAMETER Model
    Name of the model to use (e.g. gpt-3, gpt-neo, llama3), model availability is based on provider.
.PARAMETER BaseUrl
    AI Provider's base URL. 
.PARAMETER ApiKey
    API key. 
.PARAMETER Prompt
    Your prompt describing task/command to produce and execute.
.EXAMPLE
    aicommand.ps1 "list of files existing on current directory"
.EXAMPLE
    aicommand.ps1 --executor bash "list of files existing on current directory"
.SYNTAX
    aicommand.ps1 "<prompt>"
#>
[CmdletBinding()]
param (
    [Parameter(Mandatory = $true, Position = 0, ValueFromRemainingArguments = $true)]
    [String] $Prompt,
    [String] $Executor,
    [String] $Provider,
    [String] $Model,
    [String] $BaseUrl,
    [String] $ApiKey
)
$Prompt

$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition

$additionalScriptDirectory = Join-Path -Path $scriptDirectory -ChildPath script
$preScriptPath = Join-Path -Path $additionalScriptDirectory -ChildPath aicommand-pre-script.ps1

if (Test-Path -Path $preScriptPath -PathType Leaf) {
    . $preScriptPath -ScriptDirectory $scriptDirectory
}

$scriptPath = Join-Path -Path $scriptDirectory -ChildPath aicommand.py

$params = ""

if (-Not [String]::IsNullOrEmpty($Executor)) {
    $params = $params + " --executor $Executor"
}

if (-Not [String]::IsNullOrEmpty($Provider)) {
    $params = $params + " --provider $Provider"
}

if (-Not [String]::IsNullOrEmpty($Model)) {
    $params = $params + " --model $Model"
}

if (-Not [String]::IsNullOrEmpty($BaseUrl)) {
    $params = $params + " --base-url $BaseUrl"
}

if (-Not [String]::IsNullOrEmpty($ApiKey)) {
    $params = $params + " --api-key $ApiKey"
}

$pythonCommand = "python $scriptPath$params '$Prompt'"
Write-Output $pythonCommand

Invoke-Expression $pythonCommand

$postScriptPath = Join-Path -Path $additionalScriptDirectory -ChildPath aicommand-post-script.ps1

if (Test-Path -Path aicommand-post-script.ps1 -PathType Leaf) {
    . $postScriptPath
}
