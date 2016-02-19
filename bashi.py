#!/usr/bin/python
"""
Bashi Bazook
============

Bashi Bazook automates the boilerplate of Bash scripts which accept a command
as their first argument. Just give Bashi one or more Bash scripts and it will
output the necessary boilerplate to standard out.

See more docs at https://github.com/TimSimpson/BashiBazook


License
-------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import sys


START = 0
IN_FUNC = 1
CMD_START = "function cmd_"
CMD_START_LEN = len(CMD_START)


class Function(object):
    def __init__(self, name, line_number):
        self.name = name.strip().replace("_", "-")
        self.command = "cmd_" + name.strip()
        self.line_number = line_number
        self.docs = ""

    def add_doc(self, docs):
        self.docs = docs

    @property
    def summary(self):
        return self.docs.split("\n")[0]


class ScriptGenerator(object):

    def __init__(self):
        self._funcs = []

    def parse_file(self, file_path):
        line_number = 0
        current_function = None
        consume_doc = False
        with open(file_path, 'r') as f:
            for line in f:
                line_number += 1
                if (line.startswith(CMD_START)):
                    parens = line.index("(", CMD_START_LEN)
                    if parens < 0:
                        raise RuntimeError("Line %d: Don't see a start "
                            "parenthesis." % line_number)
                    name = line[CMD_START_LEN: parens]
                    current_function = Function(name, line_number)
                    self._funcs.append(current_function)
                    consume_doc = True
                elif consume_doc:
                    if line.strip().startswith("#"):
                        doc_line = line[line.find("#") + 1:].strip()
                        if current_function.docs:
                            current_function.docs += "\n" + doc_line
                        else:
                            current_function.docs = doc_line
                    else:
                        consume_doc = False

    def generate_code(self):
        print("""
bashi_base_command="${bashi_base_command:-$0}"
bashi_help_preamble="${bashi_help_preamble:-Commands :}"
bashi_exit_code_on_help="${bashi_exit_code_on_help:-1}"

function on_bashi_help() {
    # Overwrite this to change behavior.
    local hai=1
}

function bashi_help() {
    on_bashi_help
    if [ $# -lt 1 ]; then
        if [ "" != "${bashi_called_help}" ]; then
            echo "Specify a command to show help for."
        else
            echo "Usage: ${bashi_base_command} [command]"
        fi
        echo "
${bashi_help_preamble} :
            """)
        command_length = len(max(self._funcs, key=lambda f : len(f.name)).name)
        for func in self._funcs:
            pad = ' ' * (command_length - len(func.name))
            if func.summary:
                safe_summary = " - " + func.summary.replace("'", "'\"'\"'")
            else:
                safe_summary = ""
            print('    %s%s %s' % (func.name, pad, safe_summary))
        print("""
        "
    else
        case "$1" in
            """)
        for func in self._funcs:
            safe_docs = func.docs.replace("'", "'\"'\"'")
            print("            '%s' ) echo '%s' ;; " % (func.name, safe_docs))

        print("""
            * ) echo "${1} is not a valid command."
                shift
                bashi_help
        esac
    fi
    exit "${bashi_exit_code_on_help}"
}

function bashi_run() {
    # Print the available commands
    if [ $# -lt 1 ]; then
        bashi_help
        exit "${bashi_exit_code_on_help}"
    fi

    case "$1" in
        "help" ) shift; bashi_called_help=true; bashi_help $@;;
        "debug" ) shift; set -o xtrace; bashi_run $@;;
        """)

        for func in self._funcs:
            safe_docs = func.docs.replace("'", "'\"'\"'")
            print("        '%s' ) %s ;;" % (func.name, func.command))

        print("""

        * ) echo "${1} is not a valid command. Use 'help' to see all commands."
            exit 1
    esac
}
        """)


def main(args):
    script = ScriptGenerator()

    file_paths = args[1:]
    if len(file_paths) < 1:
        print("Expected one or more files to parse.")
        sys.exit(1)

    for file_path in args[1:]:
        script.parse_file(file_path)

    script.generate_code()


if __name__ == "__main__":
    main(sys.argv)



