$params = ""

for ( $i = 0; $i -lt $args.count; $i++ ) {
    $params = $params + " " + $($args[$i])
}


$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition
. $scriptDirectory\.venv\Scripts\Activate.ps1
python $scriptDirectory\aicommand.py "$params"
deactivate