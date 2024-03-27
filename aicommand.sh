#!/bin/bash

params=""

for arg in "$@"; do
    params+=" $arg"
done

scriptDirectory=$(dirname "$(realpath "$0")")
source "$scriptDirectory/.venv/Scripts/activate"
$scriptDirectory/.venv/Scripts/python "$scriptDirectory/aicommand.py" --executor bash "$params"
deactivate
