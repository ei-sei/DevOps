# Functions & Inputs
[Index](../Index.md)
## Functions

Functions are reusable blocks of code. Think of them as your own custom commands.

```bash
greet() {
    local name="$1"                    # First argument passed in
    local greeting="${2:-Hello}"        # Second argument, defaults to "Hello"

    if [[ -z "$name" ]]; then
        echo "Error: provide a name" >&2
        return 1
    fi

    echo "$greeting, $name!"
}

greet "Khaled"            # Hello, Khaled!
greet "Khaled" "Hey"      # Hey, Khaled!
greet                  # Error: provide a name
```

- `local` — keeps the variable inside the function only
- `$1`, `$2` — the first and second arguments
- `${2:-Hello}` — use "Hello" if no second argument is given
- `return 1` — signals something went wrong (0 = success, anything else = failure)

**Capturing a function's output:**

```bash
get_disk_usage() {
    df -h / | awk 'NR==2 {print $5}'
}

usage=$(get_disk_usage)
echo "Disk is $usage full"
```

---

## Argument Parsing

Let your scripts accept options like `--help` or `--quiet`.

```bash
#!/bin/bash

quiet=false
name=""

while [[ $# -gt 0 ]]; do       # While there are arguments left
    case "$1" in
        -h|--help)
            echo "Usage: myscript.sh [--name NAME] [--quiet]"
            exit 0
            ;;
        -n|--name)
            name="$2"           # Grab the next argument as the value
            shift 2             # Move past both --name and its value
            ;;
        -q|--quiet)
            quiet=true
            shift               # Move past --quiet
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

echo "Name: $name, Quiet: $quiet"
```

```bash
./myscript.sh --name Khaled --quiet    # Name: Khaled, Quiet: true
./myscript.sh --help                # Shows usage
./myscript.sh --foo                 # Unknown option: --foo
```
