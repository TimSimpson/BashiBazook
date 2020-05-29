"""
Bashi Bazook Python Helper
==========================

This reads a bash file as argument 1 containing functions beginning with
"cmd_" and returns information on it.

License
-------

MIT

"""
import sys


if False:  # check with MyPy, but keep this Py 2 compatable
    import typing as t


START = 0
IN_FUNC = 1
CMD_START = "function cmd_"
CMD_START_LEN = len(CMD_START)


class Function(object):
    def __init__(self, name, line_number):  # type: (str, int) -> None
        self.name = name.strip().replace("_", "-")
        self.command = "cmd_" + name.strip()
        self.line_number = line_number
        self.docs = ""

    def add_doc(self, docs):  # type: (str) -> None
        self.docs = docs

    @property
    def summary(self):  # type: () -> None
        return self.docs.split("\n")[0]


class Script(object):

    def __init__(self, file_path):  # type(str) -> None
        self._funcs = []  # type: t.List[str]

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

    def _get_func(self, name):  # type: (str) -> t.Optional[Function]
        for f in self._funcs:
            if f.name == name:
                return f
        return None

    def lookup_bash_function(self, name):  # type: (str) -> int
        f = self._get_func(name)
        if f:
            print(f.command)
            return 0
        else:
            return 1

    def _show_help_all(self): # type: () -> None
        if not self._funcs:
            print("""
                                       \   ^
    erm... uhm... it's empty...?      o   O  ... ?
                                       _--_-
                                        |\\\\
                                         /|    ...?!!

            """)
            return

        command_length = len(max(self._funcs, key=lambda f : len(f.name)).name)
        for func in self._funcs:
            pad = ' ' * (command_length - len(func.name))
            if func.summary:
                safe_summary = " - " + func.summary
            else:
                safe_summary = ""
            print('    {}{} {}'.format(func.name, pad, safe_summary))
        print()

    def show_help(self, name):  # type: (str) -> int
        if not name:
            if name is None:
                print("Specify a command to see more information (if available).")
            self._show_help_all()
            return 0
        else:
            f = self._get_func(name)
            if not f:
                print(
                    "{0} is not a valid command. Use 'help' to see all commands."
                    .format(name)
                )
                return 1
            else:
                print(f.docs)
                print()
                return 0


def print_usage() -> None:
    print("Usage:")
    print("     bazookp <bash_script> <subcommand> [script subcommand name]")
    print("")
    print("Subcommands:")
    print("     help")
    print("     call")


def main(args):
    if len(args) < 2:
        print("Expected a bash file to parse for argument 1.")
        print_usage()
        return 1

    script = Script(args[1])

    if len(args) < 2:
        print("Expected a subcommand for argument 2.")
        print_usage()
        return 1

    cmd = args[2]
    if cmd == 'help':
        return script.show_help(name=args[3] if len(args) >= 4 else None)
    if cmd == 'helpall':
        return script.show_help(name=False)
    elif cmd == 'lookup':
        if len(args) < 4:
            print("Expected subcommand name for argument 3.")
            print_usage()
            return 1

        name = args[3]
        return script.lookup_bash_function(name)

    print(f"Unknown command ${cmd}.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))



