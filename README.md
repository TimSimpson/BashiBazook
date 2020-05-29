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

## How it works

There's three ways of doing this.

The first involves calling "bashi_bazook.`sh", passing it` the name of your script, and then any arguments you want sent after that. Of course at this point someone might say "that's not really bash!" and gee, that could really ruin your day.

The second involves having your script source "`bashi_bazook.sh`" which lets it get called normally (though you need to make `bashi_bazook.sh` generally available or vednor `bashi_bazook.sh` and bazookp.py into your repo).

The third involves the old bashi.py script. I don't know why I'm even documenting it except I'm too lazy to delete the text for it right now.

### `bashi_bazook.sh` - call it directly

This is fall off a log easy. Just download `bashi_bazook.sh` and it's partner `bazookp.py`, stick them in the same directory somewhere, then call `bashi_bazook.sh` and pass your script as an argument.

For example:

```bash
? ./bashi_bazook.sh example.sh build
```

### `bashi_bazook.sh` - source it

This way is almost as simple. In your bash script, just source `bashi_bazook.sh` like so:


```bash
    source bashi_bazook.sh "${BASH_SOURCE[0]}" "${@}"
```

Then call it:

```bash
    ? ./example.sh build
```

##

### bashi.py

If you want to use the old method, read on. It involves vendoring only one dependency but requires temporary files.

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
