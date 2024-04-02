$params = ""

for ( $i = 0; $i -lt $args.count; $i++ ) {
    $params = $params + " " + $($args[$i])
}


$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition

$additionalScriptDirectory = Join-Path -Path $scriptDirectory -ChildPath script

$preScriptPath = Join-Path -Path $additionalScriptDirectory -ChildPath aiprompt-pre-script.ps1

if(Test-Path -Path $preScriptPath -PathType Leaf) {
    . $preScriptPath
}

$scriptPath = Join-Path -Path $scriptDirectory -ChildPath aiprompt.py

python $scriptPath "$params"

$postScriptPath = Join-Path -Path $additionalScriptDirectory -ChildPath aiprompt-post-script.ps1

if(Test-Path -Path aiprompt-post-script.ps1 -PathType Leaf) {
    . $postScriptPath
}
