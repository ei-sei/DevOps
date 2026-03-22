# Conditionals, Loops & Flow Control
[Index](../Index.md)
## Conditionals

Use `if` to make decisions in your script.

```bash
score=75

if [[ $score -gt 90 ]]; then
    echo "Excellent"
elif [[ $score -gt 50 ]]; then
    echo "Pass"
else
    echo "Fail"
fi
```

**Checking files:**

```bash
[[ -f "config.txt" ]]    # Does this file exist?
[[ -d "backups" ]]        # Does this directory exist?
[[ -s "log.txt" ]]        # Is this file non-empty?
[[ -r "data.csv" ]]       # Can I read this file?
[[ -w "output.txt" ]]     # Can I write to this file?
```

**Checking text:**

```bash
[[ -z "$name" ]]          # Is the variable empty?
[[ -n "$name" ]]          # Does the variable have a value?
[[ "$a" = "$b" ]]         # Are these two strings the same?
[[ "$a" != "$b" ]]        # Are they different?
```

**Comparing numbers:**

```bash
[[ $a -eq $b ]]           # Equal
[[ $a -ne $b ]]           # Not equal
[[ $a -lt $b ]]           # Less than
[[ $a -le $b ]]           # Less than or equal
[[ $a -gt $b ]]           # Greater than
[[ $a -ge $b ]]           # Greater than or equal
```

**Combining conditions:**

```bash
if [[ -f "app.log" ]] && [[ -r "app.log" ]]; then
    echo "Log file exists and I can read it"
fi

if [[ "$status" = "error" ]] || [[ "$status" = "failed" ]]; then
    echo "Something went wrong"
fi

if [[ ! -d "backups" ]]; then       # ! means "not"
    echo "No backups folder found"
fi
```

**Practical example — check if required tools are installed:**

```bash
for cmd in gzip tar curl; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "Missing: $cmd" >&2
    fi
done
```

---

## `[[ ]]` vs `[ ]`

You'll see both `[[ ]]` and `[ ]` in scripts. They do similar things but `[[ ]]` is safer and more powerful:

```bash
name=""

# [ ] can break if the variable is empty:
[ $name = "Bob" ]       # ERROR — becomes [ = "Bob" ] which makes no sense
[ "$name" = "Bob" ]     # Works, but you must remember the quotes

# [[ ]] handles empty variables safely:
[[ $name = "Bob" ]]     # Works fine, even without quotes
```

`[[ ]]` also supports pattern matching and regex:

```bash
[[ "$file" = *.log ]]           # Does $file end with .log?
[[ "$email" =~ ^[a-z]+@.+ ]]   # Does $email look like an email?
```

**Rule of thumb:** Use `[[ ]]` in Bash scripts. Use `[ ]` only if your script needs to work in plain `sh` (POSIX compatibility).

---

## Case Statements

When you're checking one variable against many values, `case` is cleaner than a chain of `if/elif`:

```bash
fruit="banana"

case "$fruit" in
    apple)
        echo "It's red"
        ;;
    banana)
        echo "It's yellow"
        ;;
    grape|blueberry)                # Match multiple values with |
        echo "It's purple"
        ;;
    *)                              # Default — matches anything else
        echo "I don't know that fruit"
        ;;
esac
```

**Practical example — handling a script's first argument:**

```bash
case "$1" in
    start)   start_service ;;
    stop)    stop_service ;;
    restart) stop_service; start_service ;;
    status)  show_status ;;
    *)       echo "Usage: $0 {start|stop|restart|status}" >&2; exit 1 ;;
esac
```

---

## Loops

Loops let you repeat actions.

**Do something for each item in a list:**

```bash
for fruit in apple banana cherry; do
    echo "I have a $fruit"
done
```

**Loop through files:**

```bash
for file in /var/log/*.log; do
    [[ -f "$file" ]] || continue    # Skip if not a real file
    echo "Found: $file"
done
```

**Loop a set number of times:**

```bash
for ((i = 1; i <= 5; i++)); do
    echo "Attempt $i"
done
```

**Read a file line by line:**

```bash
while IFS= read -r line; do
    echo "Line: $line"
done < names.txt
```

**Brace expansion**

```bash
for number in {1..10}; do
    echo "$number"

done
# Prints number 1-10
```

**Skipping and stopping:**

```bash
for i in {1..10}; do
    [[ $i -eq 3 ]] && continue    # Skip number 3
    [[ $i -eq 8 ]] && break       # Stop at number 8
    echo "$i"
done
# Output: 1 2 4 5 6 7
```

---

## Until Loops

`until` is the opposite of `while` — it runs *until* the condition becomes true:

```bash
count=1
until [[ $count -gt 5 ]]; do
    echo "Attempt $count"
    ((count++))
done
# Runs 5 times, then stops when count reaches 6
```

This is handy when you're waiting for something to happen:

```bash
# Wait for a server to come online
until ping -c 1 "$server" &>/dev/null; do
    echo "Waiting for $server..."
    sleep 5
done
echo "$server is up!"
```

---

## Select Menus

`select` builds a numbered menu for the user to pick from:

```bash
echo "Pick a colour:"
select colour in red green blue quit; do
    case "$colour" in
        red|green|blue)
            echo "You picked: $colour"
            ;;
        quit)
            echo "Bye!"
            break
            ;;
        *)
            echo "Invalid choice, try again"
            ;;
    esac
done
```

```
Pick a colour:
1) red
2) green
3) blue
4) quit
#? 2
You picked: green
#? 4
Bye!
```

---

## Nested Loops — `break N` and `continue N`

When you have loops inside loops, you can tell `break` or `continue` how many levels to jump:

```bash
for server in web01 web02; do
    for port in 80 443 8080; do
        if ! nc -z "$server" "$port" 2>/dev/null; then
            echo "$server:$port is down — skipping this server"
            continue 2    # Skip to the next server, not just the next port
        fi
        echo "$server:$port is up"
    done
done
```

- `break 2` — breaks out of both the inner and outer loop
- `continue 2` — skips to the next iteration of the outer loop

---

## Comparing `if`, `for`, and `while`

`if` checks a condition once, does something or doesn't:
```bash
if [[ $age -gt 18 ]]; then
    echo "Adult"
fi
# Checks once, moves on
```

`for` repeats for each item in a list. You know in advance how many times it will run:
```bash
for fruit in apple banana cherry; do
    echo "I have a $fruit"
done
# Runs exactly 3 times, then stops
```

`while` keeps repeating as long as a condition is true. You don't always know when it will stop:
```bash
count=1
while [[ $count -le 5 ]]; do
    echo "Attempt $count"
    ((count++))
done
# Keeps going until count hits 6
```

Think of it like this: `if` is a decision, `for` is a to-do list, `while` is "keep trying until".
