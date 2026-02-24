# Common Patterns & Utilities
[Index](../Index.md)
## Timestamps

```bash
date '+%Y-%m-%d %H:%M:%S'          # 2025-01-15 14:30:45
date '+%Y%m%d_%H%M%S'              # 20250115_143045 (good for filenames)
```

---

## Getting Parts of a File Path

```bash
basename "/home/sei/report.pdf"              # report.pdf (just the filename)
dirname "/home/sei/report.pdf"               # /home/sei (just the folder)
basename "/home/sei/report.pdf" .pdf         # report (filename without extension)
```

---

## Temporary Files and Directories

`mktemp` creates a unique file or directory that won't clash with anything else:

```bash
tmp_file=$(mktemp)                 # Creates something like /tmp/tmp.Xb3kR9
tmp_dir=$(mktemp -d)               # Creates a temporary directory

echo "working..." > "$tmp_file"

# Always clean up when done — pair with trap for safety
trap 'rm -f "$tmp_file"; rm -rf "$tmp_dir"' EXIT
```

---

## Logging

A simple logging function that adds timestamps and severity levels:

```bash
log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >&2
}

log INFO "Starting backup"
log WARN "Disk space is low"
log ERROR "Backup failed"
```

Output:
```
[2025-01-15 14:30:45] [INFO] Starting backup
[2025-01-15 14:30:45] [WARN] Disk space is low
[2025-01-15 14:30:46] [ERROR] Backup failed
```

**Log to both the screen and a file:**

```bash
log() {
    local level="$1"
    shift
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*"
    echo "$msg" >&2
    echo "$msg" >> "$LOG_FILE"
}

LOG_FILE="/var/log/myscript.log"
```

---

## Retry Logic

Sometimes a command fails temporarily (network issues, busy servers). Retry it a few times before giving up:

```bash
retry() {
    local max_attempts="$1"
    shift
    local attempt=1

    until "$@"; do
        if [[ $attempt -ge $max_attempts ]]; then
            echo "Failed after $max_attempts attempts: $*" >&2
            return 1
        fi
        echo "Attempt $attempt failed, retrying in 5s..." >&2
        sleep 5
        ((attempt++))
    done
}

retry 3 curl -sf "https://api.example.com/health"
```

---

## Lock Files

Prevent two copies of the same script from running at once:

```bash
LOCK_FILE="/tmp/myscript.lock"

if ! mkdir "$LOCK_FILE" 2>/dev/null; then
    echo "Another instance is already running" >&2
    exit 1
fi
trap 'rmdir "$LOCK_FILE"' EXIT

# mkdir is used because it's atomic — if two scripts race,
# only one will succeed, the other will get an error
```

---

## Text Processing Tools

These commands show up constantly in scripts. Here's what each one does:

**`grep` — find lines that match a pattern:**

```bash
grep "ERROR" app.log               # Lines containing "ERROR"
grep -i "warning" app.log          # Case-insensitive search
grep -c "ERROR" app.log            # Count matching lines
grep -v "DEBUG" app.log            # Lines that DON'T match
```

**`cut` — pull out columns from structured text:**

```bash
echo "alice:1001:/home/alice" | cut -d: -f1      # alice (field 1, split by :)
echo "alice:1001:/home/alice" | cut -d: -f1,3    # alice:/home/alice (fields 1 and 3)
```

**`sort` and `uniq` — sort lines and find duplicates:**

```bash
sort names.txt                     # Alphabetical order
sort -n numbers.txt                # Numerical order
sort -rn numbers.txt               # Reverse numerical (biggest first)
sort names.txt | uniq              # Remove consecutive duplicates
sort names.txt | uniq -c           # Count how many times each line appears
```

**`tr` — translate or delete characters:**

```bash
echo "HELLO" | tr 'A-Z' 'a-z'     # hello (lowercase)
echo "hello" | tr 'a-z' 'A-Z'     # HELLO (uppercase)
echo "a  b  c" | tr -s ' '        # a b c (squeeze repeated spaces)
```

**`awk` — do more complex text processing:**

```bash
# Print the second column (space-separated)
ps aux | awk '{print $2}'

# Print lines where column 3 is greater than 80
df -h | awk '$5+0 > 80 {print $6, "is", $5, "full"}'

# Custom field separator
echo "alice:1001" | awk -F: '{print $1}'    # alice
```

**`sed` — find and replace text:**

```bash
sed 's/old/new/' file.txt          # Replace first "old" on each line
sed 's/old/new/g' file.txt         # Replace ALL "old" on each line
sed -i 's/old/new/g' file.txt     # Edit the file in place (careful!)
sed '5d' file.txt                  # Delete line 5
```

---

## `xargs` — Turn Lines into Arguments

`xargs` takes a list of items (one per line) and passes them as arguments to a command:

```bash
# Delete all .tmp files found by find
find /tmp -name "*.tmp" | xargs rm -f

# Same thing, but handles filenames with spaces
find /tmp -name "*.tmp" -print0 | xargs -0 rm -f

# Run a command on each item one at a time
cat servers.txt | xargs -I {} ssh {} "uptime"
# {} is replaced with each line from the list
```

---

## Checking Prerequisites

Before your script does real work, make sure everything it needs is available:

```bash
check_requirements() {
    local missing=()

    for cmd in curl jq gzip; do
        if ! command -v "$cmd" &>/dev/null; then
            missing+=("$cmd")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Missing required tools: ${missing[*]}" >&2
        return 1
    fi
}

check_requirements || exit 2
```
