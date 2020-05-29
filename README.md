# Bashi Bazook

Bashi Bazook automates the boilerplate of Bash scripts which accept a command
as their first argument. Just write Bash scripts with functions starting with "cmd_" and you'll automatically be able to run them as subcommands as well as get a decent menu showing what's available.

For example, let's say you write a bash script like this:

```bash
    function cmd_build() {
        # builds the project
        #
        # First, make sure that blah blah blah...
        echo 'Invoking build...'
        ...
    }
```

With Bashi Bazook, you can see what's available by invoking the script with no commands:

```bash
    ? ./example.sh
    Usage: ./example.sh [command]

    Commands :
        build  - builds the project
```

execute the command by passing "build":

```bash
    ? ./example.sh build
    Invoking build...
```

and see help using the built in "help" command:

```bash
    ? ./example.sh help build
    builds the project

    First, make sure that blah blah blah...
```

You can easily write all of the code to make a menu, call different functions, show help etc in Bash yourself. I know because I've done so many times. Bashi is an attempt to simplify that. I consider it a quasi-alternative to tools such as [ok-bash](http://www.secretgeek.net/ok) and [frontdoor](https://github.com/TimSimpson/frontdoor).


## How it works

There's three ways of using Bashi Bazook.

### `bashi_bazook.sh` - call it directly

Download `bashi_bazook.sh` and its partner `bazook.py` and stick them in the same directory somewhere. Then pass the name of your script and any arguments you want sent to said script.

For example:

```bash
? ./bashi_bazook.sh example.sh build
```

Of course at this point someone might say "that's not really bash!" and gee, that could really ruin your day.

### `bashi_bazook.sh` - source it

This way is almost as simple. Again, download `bashi_bazook.sh` and `bazook.py`into the same directory. Then in your bash script, just source `bashi_bazook.sh` like so:


```bash
    source bashi_bazook.sh "${BASH_SOURCE[0]}" "${@}"
```

Then call it like it was a normal bash script:

```bash
    ? ./example.sh build
```
### invoke `bashi.py` then source the generated bash script

This method involves vendoring only one file but it also creates a temporary file.

First, make bashi.py available.
In your own script, you add the following:

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

Bashi allows for documentation. Just add a pound sign right after a function:

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
