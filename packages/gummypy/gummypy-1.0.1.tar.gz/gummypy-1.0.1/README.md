# Gummypy
A small library that contains wrapper functions around the [gum](https://github.com/charmbracelet/gum) CLI tool.

# Usage
Below is an example on how to use the `choose` function. All wrappers of each subcommand in `gum` are in a class called `GumWrappers`

```python
# `GumWrappers` is a class that only has static methods (classmethods) of each subcommands of `gum` 
from gummypy import GumWrappers

# entrypoint
def main():
    # Runs `gun choose --limit=2 "foo" "bar" "baz"` in the terminal
    GumWrappers.choose(["foo", "bar", "baz"], limit=2)

if __name__ == "__main__":
    main()
```
