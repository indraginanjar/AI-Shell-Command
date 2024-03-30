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
. $scriptDirectory\.venv\Scripts\Activate.ps1

if ($args.Count -eq 3 -and ($args[0] -eq '--executor' -or $args[0] -eq '-executor')) {
    [String] $executor = $args[1]
    [String] $prompt = $args[2]
    python $scriptDirectory\aicommand.py --executor $executor "$prompt"

} else {
    $params = ""

    for ( $i = 0; $i -lt $args.count; $i++ ) {
        $params = $params + " " + $($args[$i])
    }
    
    python $scriptDirectory\aicommand.py "$params"
}

deactivate