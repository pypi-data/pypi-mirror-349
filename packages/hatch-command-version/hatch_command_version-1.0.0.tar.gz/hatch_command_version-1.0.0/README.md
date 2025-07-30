# hatch-command-version

A version source plugin to the `hatchling.build` python build backend that obtains a version by running a command.

```.toml
[build-system]
requires = [
    "hatchling",
    "hatch-command-version",        # pull in this plugin
]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "command"                   # pick this version source plugin
command = "path/to/custom-generator" # the command to execute
```
