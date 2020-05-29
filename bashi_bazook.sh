#!/bin/bash

readonly bazook_source="${BASH_SOURCE[0]}"
while [ -h "${bazook_source}" ]; do
  bazook_root_dir="$( cd -P "$( dirname "${bazook_source}" )" >/dev/null 2>&1 && pwd )"
  bazook_source="$(readlink "${bazook_source}")"
  [[ "${bazook_source}" != /* ]] && bazook_source="${bazook_root_dir}/${bazook_source}"
done
bazook_root_dir="$( cd -P "$( dirname "${bazook_source}" )" >/dev/null 2>&1 && pwd )"

readonly bazook_python_helper="${bazook_root_dir}/bazookp.py"

readonly bazook_name="${0}"

if [ $# -lt 1 ]; then
    echo 'Expected a script.'
    exit 1
fi

readonly bazook_script_arg="${1}"

shift 1;


# Figure out if we need to source the argument script or if it is sourcing us.
read bazook_caller_line bazook_caller_sub bazook_caller_file < <(caller 0)

# Source the script, unless it sourced us.
if [ "${bazook_caller_file}" != "${bazook_script_arg}" ]; then
    source "${bazook_script_arg}"
    bashi_base_command="${bashi_base_command:-'${bazook_name}' '${bazook_script_arg}'}"
else
    bashi_base_command="${bashi_base_command:-'${bazook_script_arg}'}"
fi

# Override this to show custom help stuff.
bazook_help_preamble="${bazook_help_preamble:-Commands :}"


function bazookp(){
    python "${bazook_python_helper}" "${bazook_script_arg}" "${@}"
}

function bazook_call(){
    cmd="${1}"
    shift 1
    local function_name=$(bazookp lookup "${cmd}")
    if [ "${function_name}" == "" ]; then
        echo "'${cmd}' is not a valid command. Use 'help' to see all commands."
        exit 1
    else
        "${function_name}" "${@}"
    fi
}

if [ $# -lt 1 ]; then
    # echo "Usage: ${bazook_name} ${bazook_script_arg} [command]"
    echo "Usage: ${bashi_base_command} [command]"
    echo
    echo "${bazook_help_preamble}"
    bazookp helpall
    exit  1
fi

case "$1" in
    "help" ) shift; bazookp help "${@}";;
    * ) bazook_call "${@}"
esac
