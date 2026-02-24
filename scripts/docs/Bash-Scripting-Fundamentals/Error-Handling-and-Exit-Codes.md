# Error Handling & Exit Codes
[Index](../Index.md)
## Exit Codes

Every command returns an exit code: **0 means success**, anything else means failure.

```bash
return 0    # Success (inside a function)
return 1    # Failure (inside a function)

exit 0      # Success (exits the entire script)
exit 1      # Failure (exits the entire script)
```

Use `return` inside functions and `exit` at the script level.

---

## Checking if a Command Succeeded

The special variable `$?` holds the exit code of the last command that ran:

```bash
grep -q "error" /var/log/app.log
echo $?    # 0 if "error" was found, 1 if not
```

You can use it in conditionals:

```bash
cp important.txt /backup/
if [[ $? -ne 0 ]]; then
    echo "Backup failed!" >&2
    exit 1
fi
```

But it's cleaner to put the command directly in the `if`:

```bash
if ! cp important.txt /backup/; then
    echo "Backup failed!" >&2
    exit 1
fi
```

**Quick one-liners with `&&` and `||`:**

```bash
mkdir /backup && echo "Created"     # Run echo only if mkdir succeeded
mkdir /backup || echo "Failed"      # Run echo only if mkdir failed

cd /app || { echo "Can't find /app" >&2; exit 1; }    # Bail out on failure
```

---

## Safety Options with `set`

These options catch common mistakes early, before they cause bigger problems. Put them near the top of your script:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

Here's what each one does:

**`set -e` — stop on errors:**

Normally Bash keeps running even when a command fails. This makes it stop immediately:

```bash
set -e
cp file.txt /backup/       # If this fails...
echo "Backup done"         # ...this line never runs
```

Without `set -e`, the script would keep going and pretend everything is fine.

**`set -u` — catch typos in variable names:**

Normally, using an undefined variable silently gives you an empty string. This makes it an error instead:

```bash
set -u
echo "Hello, $naem"        # ERROR — did you mean $name? Bash catches the typo
```

**`set -o pipefail` — catch failures in pipes:**

Normally, a pipe only reports the exit code of the *last* command. This makes it report failure if *any* command in the pipe fails:

```bash
set -o pipefail
bad_command | sort | head   # Without pipefail: exit code 0 (from head)
                            # With pipefail: exit code non-zero (from bad_command)
```

---

## Automatic Cleanup with `trap`

`trap` lets you run cleanup code when your script finishes — even if it crashes:

```bash
cleanup() { rm -f "$tmp_file"; }
trap cleanup EXIT                   # Runs cleanup on exit, even if the script fails

tmp_file=$(mktemp)                  # Create a temporary file
echo "working..." > "$tmp_file"
# When the script ends, the temp file is automatically deleted
```

**You can trap different signals:**

```bash
trap 'echo "Caught Ctrl+C, cleaning up..."; cleanup; exit 1' INT    # Ctrl+C
trap 'echo "Script finished"; cleanup' EXIT                          # Any exit
trap 'echo "Error on line $LINENO" >&2' ERR                          # Any error
```

**Practical example — safe temporary directory:**

```bash
work_dir=$(mktemp -d)
trap 'rm -rf "$work_dir"' EXIT

# Do all your work inside $work_dir
# It gets cleaned up automatically, no matter how the script ends
```

---

## Debugging

When things go wrong, these tools help you figure out why.

**`set -x` — show every command as it runs:**

```bash
set -x                      # Turn on tracing
name="world"
echo "Hello, $name"
set +x                      # Turn off tracing
```

Output:
```
+ name=world
+ echo 'Hello, world'
Hello, world
+ set +x
```

Each line starting with `+` shows you exactly what Bash is doing. This makes it easy to spot where things go wrong.

**Print the line number where an error happened:**

```bash
trap 'echo "Error at line $LINENO" >&2' ERR
```

**Debug a specific section without tracing everything:**

```bash
# ... normal code ...

set -x    # Start tracing
problematic_function
set +x    # Stop tracing

# ... normal code continues ...
```
