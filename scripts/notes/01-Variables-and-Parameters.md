# Variables & Parameters
[Index](../Index.md)
## Variables

Variables store information you want to reuse.

```bash
name="servers"                     # Store text (NO spaces around =)
count=42                           # Store a number
today=$(date '+%Y-%m-%d')          # Store the output of a command

echo "Managing: $name"             # Double quotes — fills in the variable
echo 'Managing: $name'             # Single quotes — prints it literally

export ENV="production"            # Makes the variable available to other scripts
readonly MAX=3                     # Can't be changed once set
```

**Key rule:** Always wrap variables in double quotes `"$var"` not `$var`. Without quotes, filenames with spaces will break your script.

```bash
# Why quoting matters:
file="my report.txt"
cat $file      # WRONG — tries to open "my" and "report.txt" separately
cat "$file"    # RIGHT — opens "my report.txt"
```

---

## Arithmetic

Bash doesn't do math on its own, you need `$(( ))` to tell it "this is a calculation":

```bash
a=10
b=3

echo $((a + b))       # 13
echo $((a - b))       # 7
echo $((a * b))       # 30
echo $((a / b))       # 3  (integer only — no decimals)
echo $((a % b))       # 1  (remainder)
echo $((a ** 2))      # 100 (power)
```

You can also increment and decrement:

```bash
count=0
((count++))           # count is now 1
((count += 5))        # count is now 6
```

---

## Arrays

Arrays let you store a list of values in a single variable.

**Creating and using arrays:**

```bash
fruits=("apple" "banana" "cherry")

echo "${fruits[0]}"         # apple (first item — arrays start at 0)
echo "${fruits[1]}"         # banana
echo "${fruits[@]}"         # apple banana cherry (all items)
echo "${#fruits[@]}"        # 3 (how many items)
```

**Adding and removing items:**

```bash
fruits+=("grape")           # Add to the end
unset 'fruits[1]'           # Remove banana (leaves a gap)
```

**Looping through an array:**

```bash
servers=("web01" "web02" "db01")

for server in "${servers[@]}"; do
    echo "Checking $server..."
done
```

---

## Parameters

Parameters are how you pass information into a script or function.

```bash
# If you run: ./myscript.sh hello world

$0    # ./myscript.sh  (the script name)
$1    # hello           (first argument)
$2    # world           (second argument)
$#    # 2               (how many arguments were passed)
$@    # hello world     (all arguments, as separate words)
$*    # hello world     (all arguments, as one single string)
```

**`$@` vs `$*` — when it matters:**

Most of the time they look the same, but inside double quotes they behave differently:

```bash
# If you run: ./test.sh "hello world" foo

"$@"   # → "hello world" "foo"    (keeps each argument separate — 2 items)
"$*"   # → "hello world foo"      (smashes everything into one string — 1 item)
```

Use `"$@"` when passing arguments along to another command, it preserves spacing:

```bash
# Pass all arguments to another script, keeping each one intact
other_script.sh "$@"
```

**Simple example:**

```bash
#!/bin/bash
echo "Script: $0"
echo "First: $1"
echo "Second: $2"
echo "Total args: $#"
```

```bash
./greet.sh hello Khal
# Script: ./greet.sh
# First: hello
# Second: Khal
# Total args: 2
```

---

## Parameter Expansion

Bash has built-in shortcuts for working with variable values, no need for external tools.

**Defaults — fill in a value if the variable is empty:**

```bash
name="${1:-Guest}"          # Use "Guest" if $1 wasn't provided
echo "Hello, $name"
```

**String length:**

```bash
path="/home/sei/documents"
echo "${#path}"             # 20 (number of characters)
```

**Chopping parts off a string:**

```bash
file="backup.2025-01-15.tar.gz"

echo "${file%.tar.gz}"      # backup.2025-01-15   (remove shortest match from end)
echo "${file%%.*}"          # backup              (remove longest match from end)
echo "${file#*.}"           # 2025-01-15.tar.gz   (remove shortest match from start)
echo "${file##*.}"          # gz                  (remove longest match from start)
```

**Search and replace:**

```bash
msg="hello world world"

echo "${msg/world/earth}"   # hello earth world   (replace first match)
echo "${msg//world/earth}"  # hello earth earth   (replace all matches)
```

**Substrings:**

```bash
text="abcdefgh"
echo "${text:2:4}"          # cdef  (start at position 2, take 4 characters)
```
