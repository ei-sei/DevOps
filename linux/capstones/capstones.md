## Capstone 1: The Mysterious Slow Server

**Scenario:** Users complain the website is slow. Diagnose the issue.

**Tasks:**
1. Check uptime and load
2. Find top CPU/memory consumers
3. Check disk space
4. Review recent logs
5. Document findings

**Solution Framework:**

```bash
#!/bin/bash

# Colors for highlighting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== INVESTIGATION REPORT ===${NC}"
echo -e "${GREEN}Date: $(date)${NC}"
echo -e "${GREEN}Host: $(hostname)${NC}\n"

echo -e "${YELLOW}---- UPTIME ----${NC}"
uptime
echo

echo -e "${YELLOW}---- MEMORY ----${NC}"
free -h
echo

echo -e "${YELLOW}---- DISK USAGE ----${NC}"
df -h /
echo

echo -e "${YELLOW}---- TOP 5 CPU PROCESSES ----${NC}"
ps aux --sort=-%cpu | head -6
echo

echo -e "${YELLOW}---- LAST 50 SYSLOG ERRORS ----${NC}"
sudo tail -50 /var/log/syslog | grep -i error \
    | while read -r line; do
        echo -e "${RED}$line${NC}"
      done || echo "No recent syslog errors found"
echo

echo -e "${YELLOW}---- LAST 50 JOURNAL ERRORS ----${NC}"
sudo journalctl -p err -n 50 --no-pager \
    | while read -r line; do
        echo -e "${RED}$line${NC}"
      done || echo "No recent journal errors found"
echo

echo -e "${YELLOW}=== END OF REPORT ===${NC}"

```
Breakdown:

- Colors – The script uses ANSI color codes to make the output easy to scan:
- Red = errors/warnings

- Yellow = section headers

- Green = general info

- Sections – Each section gathers different system metrics or logs:

- Date/Host → metadata for the report

- Uptime → system load and running time

- Memory → current RAM and swap usage

- Disk usage → free and used space on root /

- Top CPU processes → quickly identify any resource hogs

- Syslog errors → filtered recent errors

- Journal errors → systemd-managed logs for errors

- Log highlighting – The script loops through each error line and prints it in red for quick visibility.

- Fail-safes – If there are no recent errors, it prints “No recent syslog/journal errors found.”

- Usage – Save, make executable (chmod +x script.sh), and run (./script.sh). Can redirect output to a file if needed:

---

## Capstone 2: User On-boarding

**Scenario:** Create accounts for alice, bob, charlie with shared project access.

**Solution Framework:**

```bash
sudo groupadd developers
for user in alice bob charlie; do
    sudo useradd -m -s /bin/bash -G developers $user
done
sudo mkdir -p /tmp/project
sudo chown root:developers /tmp/project
sudo chmod 2775 /tmp/project
```

---

## Capstone 3: Disk Space Emergency

**Scenario:** Root file system at 90%. Find and clean space.

**Solution Framework:**

```bash
df -h /
sudo du -sh /var/* | sort -h | tail -10
sudo find /var/log -name "*.log*" -mtime +7
sudo apt clean
sudo apt autoremove
```

---

## Capstone 4: Security Quick Audit

**Solution Framework:**

```bash
echo "=== SECURITY AUDIT ==="
echo "Users with login shells:"
grep -E "/bin/bash|/bin/sh" /etc/passwd

echo "Users with UID 0:"
awk -F: '$3 == 0 {print $1}' /etc/passwd

echo "Listening services:"
ss -tulnp

echo "Sudo users:"
grep sudo /etc/group
```

---