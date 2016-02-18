# Bashi Bazook

Bashi Bazook automates the boilerplate of Bash scripts which accept a command
as their first argument. Just give Bashi one or more Bash scripts and it will
output the necessary boilerplate to standard out.

## How it works

When Bashi finds lines that begin like the following:

```bash
    function cmd_build() {
```

it records them and creates some dispatch code like this:

```bash

function bashi_run() {
    # Print the available commands
    if [ $# -lt 1 ]; then
        bashi_help
        exit "${bashi_exit_code_on_help}"
    fi

    case "$1" in
        "help" ) shift; bashi_called_help=true; bashi_help $@;;
        "debug" ) shift; set -o xtrace; bashi_command $@;;

        "build" ) cmd_build $@;;


        * ) echo "${1} is not a valid command. Use 'help' to see all commands."
            exit 1
    esac
}
```

In your own script, you then add the following:

```bash

# It's Morphoid time.

function cmd_refresh () {
    python bashi.py my-script.sh > my-script.bashi
}

set +e
source my-script.bashi || cmd_refresh
set -e
source my-script.bashi

bashi_run $@

```

This has a side effect of creating the command "refresh" which will re-generate
the Bashi components of your script.

## Documentation

Bashi also allows for documentation. Just add a pound sign a function:

```bash
function cmd_build() {
    # Builds the project.
    #
    # Accepts arguments to be passed to make. Back in 1974, this project was ...
```

Bashi produces a command called "help" which, if given zero arguments, will
print out a list of all available commands. This list will only show the first
comment- in this case, "Builds the project."

If help is passed the name of a command, it will print out the entirety of the
comment.

## Inserting in Your Project

Bashi is licensed under Apache 2. Feel free to either add it to your path, or
to simply copy the Python script to your source.


## Why use Bash?

All projects need a "front door" script which makes it simple to do common
things. The alternative is to document how to do all these things which
is the antithesis of automation.

For example, Java projects can use Maven, Ant, or Kobalt, C++ projects
might use CMake, Scons, Meson, or Bjam, Python projects can use Fabric, Paver,
etc etc... you get the idea.

All of these tools come with their own opinions, most of which are
highly invested in the ecosystem which bore them. Often times, you may be blind
to these opinions depending on how long you've spent in a particular ecosystem.

For example, nuget is awesome, but only if you live and breathe .NET. CMake is
great, but only if you remember the magical spells you must invoke to cleanly
build for the target platform of choice without polluting your source directory.
Maven is great as long as your cool installing the 900 pound Gorilla that is
the JVM on a particular machine. Etc, etc.

The biggest problem is that often teams create an edict saying they'll
only use one such tool. When they do that they effectively lock themselves into
a mindset that the tool cannot be wrong and spend ages working around
shortcomings. If you've ever seen people spend man-years writing custom plugins
for Maven to execute one or two commands they could invoke by hand you'll
know what I'm talking about. When the time involved to work around a tool's
problems (just so you can do things "the right way" according to your current
religion) outweighs the effort of just telling people the few extra commands
they need to run by hand, the team responds by avoiding automation for "simple
things." These little things add up, and soon you have a situation where
people are all pointing fingers at who forgot to document what. IMO the root
problem though is even trivial steps like this shouldn't just be documented,
they should be automated.

Bash suffers from fewer opinions than any tool I've used,
*particularly* (only?) when you resolve yourself to make such scripts short and
focused solely on bootstrapping environments to call other higher level tools.
This frees you up to follow the old often-stated but rarely heeded adage of
always using the right tool for the job.

Front-door scripts written using Bash also turn out fairly pretty,
as they perfectly resemble a terminal session (for obvious reasons).
Additionally Bash is a real language, and contains some decent features such as
readonly variables and error trapping that may surprise the uninitiated.

Finally, Bash is shockingly portable - at least as much as something like this
can be. It comes installed by default on *nix systems and is installed with
Git for Windows. But its biggest selling point is that it doesn't screw up
the invocation of commands. For  example, Fabric is a neat tool, but doesn't
work on Windows or Python 3. Bjam is a nice tool but when it invokes Clang it
prevents the pretty colors from showing. Other tools cause programs that print
a lot to standard out to run slower. Bash suffers from no problems such as
this.


## License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

