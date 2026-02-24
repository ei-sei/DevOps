### Real-World Context
When something goes wrong; high CPU, memory exhaustion. You need to quickly identify problematic processes. This is often the first thing you'll do during an incident.

### Windows ↔ Linux Bridge

| Windows          | Linux                | Notes              |
| ---------------- | -------------------- | ------------------ |
| Task Manager     | `top`, `htop`, `ps`  | Process viewer     |
| End Task         | `kill`               | Terminate process  |
| services.msc     | `systemctl`          | Service management |
| Resource Monitor | `top`, `vmstat`      | Resource monitoring|

### Core Commands Reference

| Command      | Purpose            | Example                 |
| ------------ | ------------------ | ----------------------- |
| `ps aux`     | All processes      | `ps aux`                |
| `top`        | Real-time viewer   | `top` (q to quit)       |
| `kill`       | Send signal        | `kill PID`              |
| `kill -9`    | Force kill         | `kill -9 PID`           |
| `killall`    | Kill by name       | `killall firefox`       |
| `pgrep`      | Find PID           | `pgrep nginx`           |
| `systemctl`  | Service management | `systemctl status nginx`|
| `free -h`    | Memory usage       | `free -h`               |
| `df -h`      | Disk space         | `df -h`                 |
| `du -sh`     | Directory size     | `du -sh /var/*`         |
| `uptime`     | System uptime      | `uptime`                |

### Challenges:
---
 
**Challenge 3.1: Finding Resource-Heavy Processes**

_Solution:_
```bash
# Top 5 by CPU
ps aux --sort=-%cpu | head -6

# Top 5 by memory
ps aux --sort=-%mem | head -6
```

---

**Challenge 3.2: Managing Background Processes**

_Solution:_
```bash
sleep 60 &          # Starts a 60-second process in the background.
jobs                # Lists all jobs started from this shell.
fg %1               # Brings job 1 to the foreground.
# Ctrl+Z to suspend # Temporarily pauses the foreground job.
bg %1               # Resumes job 1 running in the background.

```


---

**Challenge 3.3: Keeping Processes Running After Logout**

_Solution:_
```bash
nohup ./long_script.sh &
# Output goes to nohup.out
tail -f nohup.out
```

---

**Challenge 3.4: Killing Processes**

_Solution:_
```bash
sleep 300 &
pgrep sleep
kill PID            # Graceful (SIGTERM)
kill -9 PID         # Force (SIGKILL) - last resort
```

---

**Challenge 3.5: System Resource Overview**

_Solution:_
```bash
uptime              # Load averages
free -h             # Memory
df -h               # Disk space
sudo du -sh /var/*  # Directory sizes
```

---

