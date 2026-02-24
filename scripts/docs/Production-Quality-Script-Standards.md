### Production-Quality Script Standards
[Index](/Index.md)

Every script must include:

**1. Shebang Line**

```bash
#!/usr/bin/env bash    # Bash scripts
#!/usr/bin/env python3 # Python scripts
```

Using `env` makes scripts portable — it finds the interpreter wherever it's installed.

**2. Header Comment**

```bash
#!/usr/bin/env bash
#
# Script: system-health-check.sh
# Purpose: Monitor CPU, memory, and disk usage with configurable thresholds
# Author: Your Name
# Date: 2026-XX-XX
# Version: 1.0
#
# Usage:
#   ./system-health-check.sh [OPTIONS]
#   ./system-health-check.sh -c 90 -m 85 -d 75
#
# Dependencies:
#   - free (part of procps)
#   - df (part of coreutils)
```

**3. Command-Line Arguments** — never hard-code values that might change:

```bash
# Good: configurable
./backup.sh --source /home/user --destination /backup --keep 7
# Bad: hard-coded
./backup.sh   # always backs up /etc to /tmp
```

**4. Error Handling** — check prerequisites, handle failures:

```bash
if ! command -v gzip &>/dev/null; then
    echo "ERROR: gzip is required but not installed" >&2
    exit 2
fi
```

**5. Logging** — timestamped so you can debug issues after the fact:

```bash
log() {
    local level="$1" message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
}
```

**6. Comments** — explain _why_, not _what_:

```bash
# Bad: Increment counter
counter=$((counter + 1))
# Good: Track failed services for the summary report
counter=$((counter + 1))
```

### Exit Codes Convention

|Code|Meaning|
|---|---|
|0|Success|
|1|General error|
|2|Missing dependency/prerequisite|
|3|Invalid arguments|
|4|Permission denied|
|5|Resource not found|
