<#
.SYNOPSIS
    Powershell/pwsh aicommand
.DESCRIPTION
    Powershell script for running aicommand.py
.PARAMETER Executor
    Target application/shell/language 
.PARAMETER prompt
    Your prompt describing task/command to produce and execute.
.EXAMPLE
    aicommand.ps1 "list of files existing on current directory"
.EXAMPLE
    aicommand.ps1 --executor bash "list of files existing on current directory"
.SYNTAX
    aicommand.ps1 <--executor <executor>> "<prompt>"
#>

$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition

$additionalScriptDirectory = Join-Path -Path $scriptDirectory -ChildPath script

$preScriptPath = Join-Path -Path $additionalScriptDirectory -ChildPath aicommand-pre-script.ps1

if(Test-Path -Path $preScriptPath -PathType Leaf) {
    . $preScriptPath
}

$scriptPath = Join-Path -Path $scriptDirectory -ChildPath aicommand.py

if ($args.Count -eq 3 -and ($args[0] -eq '--executor' -or $args[0] -eq '-executor')) {
    [String] $executor = $args[1]
    [String] $prompt = $args[2]

    python $scriptPath --executor $executor "$prompt"

} else {
    $params = ""

    for ( $i = 0; $i -lt $args.count; $i++ ) {
        $params = $params + " " + $($args[$i])
    }
    
    python $scriptPath "$params"
}

$postScriptPath = Join-Path -Path $additionalScriptDirectory -ChildPath aicommand-post-script.ps1

if(Test-Path -Path aicommand-post-script.ps1 -PathType Leaf) {
    . $postScriptPath
}
