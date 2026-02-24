### Real-World Context

Logs tell the story when something breaks. DevOps engineers spend significant time analyzing logs to troubleshoot issues.

### Windows ↔ Linux Bridge

| Windows                  | Linux          | Notes            |
| ------------------------ | -------------- | ---------------- |
| Event Viewer             | `/var/log/`    | Log locations    |
| `findstr`                | `grep`         | Search text      |
| `type`                   | `cat`          | Display file     |
| PowerShell Select-String | `grep`, `awk`  | Pattern matching |

### Core Commands Reference

| Command     | Purpose            | Example                      |
| ----------- | ------------------ | ---------------------------- |
| `cat`       | Display file       | `cat file.txt`               |
| `less`      | Page through       | `less file.log`              |
| `head -n 20`| First 20 lines     | `head -20 file`              |
| `tail -n 50`| Last 50 lines      | `tail -50 file`              |
| `tail -f`   | Follow real-time   | `tail -f /var/log/syslog`    |
| `grep`      | Search pattern     | `grep "error" file.log`      |
| `grep -i`   | Case insensitive   | `grep -i "error" file`       |
| `grep -c`   | Count matches      | `grep -c "error" file`       |
| `grep -v`   | Invert/exclude     | `grep -v "debug" file`       |
| `sed`       | Search/modify files| `sed 's/old/new/g' file.txt` |
| `sort`      | Sort lines         | `sort file.txt`              |
| `uniq`      | Remove duplicates  | `sort file \| uniq`          |
| `awk`       | Extract fields     | `awk '{print $1}' file`      |
| `wc -l`     | Count lines        | `wc -l file.txt`             |

### Understanding Pipes

Pipes (`|`) connect commands:

```bash
grep "404" access.log | wc -l
# Finds 404 errors and counts them
```

### Challenges:
---

First, create sample logs:

```bash
mkdir -p ~/log-lab && cd ~/log-lab

cat << 'EOF' > access.log
192.168.1.100 - - [15/Jan/2024:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 1234
192.168.1.101 - - [15/Jan/2024:10:15:33 +0000] "GET /style.css HTTP/1.1" 200 567
192.168.1.100 - - [15/Jan/2024:10:15:34 +0000] "GET /api/users HTTP/1.1" 500 89
10.0.0.50 - - [15/Jan/2024:10:15:35 +0000] "POST /login HTTP/1.1" 401 45
10.0.0.50 - - [15/Jan/2024:10:15:37 +0000] "POST /login HTTP/1.1" 401 45
10.0.0.50 - - [15/Jan/2024:10:15:39 +0000] "POST /login HTTP/1.1" 401 45
192.168.1.103 - - [15/Jan/2024:10:15:40 +0000] "GET /favicon.ico HTTP/1.1" 404 0
192.168.1.100 - - [15/Jan/2024:10:15:42 +0000] "GET /api/orders HTTP/1.1" 500 76
EOF
```

---
 
**Challenge 4.1: Following Logs in Real-Time**

_Solution:_
```bash
tail -f access.log
# Ctrl+C to stop
```

---

**Challenge 4.2: Searching Log Files**

_Solution:_

```bash
grep "500" access.log           # Find 500 errors
grep -c "500" access.log        # Count them
grep -B 2 -A 2 "500" access.log # With context

# Replace "500" with "SERVER_ERROR" (does not change the file)
sed 's/500/SERVER_ERROR/g' access.log   
```

---

**Challenge 4.3: Finding Unique Values**

_Solution:_

```bash
# Unique IPs sorted by request count
awk '{print $1}' access.log | sort | uniq -c | sort -rn
```

Breakdown:
- `awk '{print $1}' access.log` extracts the IP addresses from the log file.

- `sort` orders the IP addresses so identical ones are grouped together.

- `uniq -c` counts how many times each IP appears.

- `sort -rn` sorts the results from highest to lowest request count.

---

**Challenge 4.4: Parse /etc/passwd to list all users with /bin/bash as their shell**

_Solution:_

```bash
grep '/bin/bash$' /etc/passwd

```

---

**Challenge 4.5: Log Analysis Report**

_Solution:_

```bash
echo "=== LOG ANALYSIS ==="
echo "Total requests: $(wc -l < access.log)"
echo ""
echo "By status code:"
awk '{print $9}' access.log | sort | uniq -c | sort -rn
echo ""
echo "By IP (top 5):"
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5
```
---

