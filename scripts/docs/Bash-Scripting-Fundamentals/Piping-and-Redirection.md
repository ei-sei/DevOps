# Piping & Redirection
[Index](../Index.md)
## The Three Streams

Every command has three channels for data, called "file descriptors":

```
            ┌─────────┐
 stdin (0) ─→│         │─→ stdout (1)   (normal output)
             │ command │
             │         │─→ stderr (2)   (error messages)
             └─────────┘
```

- **stdin (0)** — input going *into* the command (keyboard, or data piped in)
- **stdout (1)** — normal output (what you see when things work)
- **stderr (2)** — error messages (kept separate so they don't mix with real output)

```bash
echo "All good"                # Goes to stdout (stream 1)
echo "Something broke" >&2     # Goes to stderr (stream 2)
```

---

## Output Redirection

**Writing to files:**

```bash
echo "first line" > file.txt    # Creates or overwrites the file
echo "second line" >> file.txt  # Appends to the end of the file
```

**Redirecting stdout and stderr separately:**

```bash
./script.sh > output.log          # Save normal output, errors still show on screen
./script.sh 2> errors.log         # Save errors only, normal output still shows
./script.sh > output.log 2> errors.log   # Save them into separate files
```

**Redirecting both to the same place:**

```bash
./script.sh > all.log 2>&1        # Send errors to wherever stdout is going (the file)
./script.sh &> all.log            # Shorthand — same thing, cleaner to read
./script.sh &>/dev/null           # Throw away all output entirely
```

The `2>&1` part means "send stream 2 (stderr) to the same place as stream 1 (stdout)". Order matters — the redirect to the file must come first.

---

## Input Redirection

**Reading from a file instead of the keyboard:**

```bash
wc -l < names.txt                # Count lines — feeds the file into wc's stdin
sort < unsorted.txt > sorted.txt # Read from one file, write to another
```

**Here-documents — embed multi-line text directly in your script:**

```bash
cat <<EOF
Hello $USER,
Today is $(date '+%A').
Welcome to the system.
EOF
```

This sends everything between `<<EOF` and `EOF` as input. Variables and commands inside get expanded.

Use `<<'EOF'` (with quotes) to prevent expansion:

```bash
cat <<'EOF'
This prints $USER literally, not your username.
No expansion happens here.
EOF
```

**Here-strings — send a single string as input:**

```bash
grep "error" <<< "$log_output"    # Search through a variable's contents
bc <<< "3.14 * 2"                 # Quick math with decimals
```

---

## Piping

A pipe (`|`) sends one command's stdout into the next command's stdin:

```bash
cat names.txt | grep "Smith" | wc -l
# Read the file → filter for "Smith" → count the matches
```

Think of it as an assembly line — each command does one job and passes the result along.

**More examples:**

```bash
# Find the 5 biggest files in a directory
du -sh /var/log/* | sort -rh | head -5

# Show unique error types from a log, sorted by frequency
grep "ERROR" app.log | awk '{print $4}' | sort | uniq -c | sort -rn

# List running processes and search for one
ps aux | grep "nginx"
```

---

## Tee — Save and Display at the Same Time

`tee` splits the stream — it writes to a file *and* passes the output through:

```bash
./build.sh | tee build.log
# You see the output on screen AND it's saved to build.log

./deploy.sh 2>&1 | tee -a deploy.log
# Append (-a) everything (stdout + stderr) to the log while watching it live
```

This is useful for commands you want to monitor *and* keep a record of.

---

## Process Substitution

Sometimes you want to feed the output of a command where a filename is expected. Process substitution `<(command)` makes it look like a file:

```bash
# Compare the output of two commands side by side
diff <(ls /dir1) <(ls /dir2)

# Both sides are treated as if they were files, but they're actually command outputs
```

**Practical example — compare sorted and unsorted lists:**

```bash
diff <(sort file.txt) <(sort -u file.txt)
# Shows which lines are duplicated (sort vs sort-unique)
```
