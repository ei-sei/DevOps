# Linux Lab Notebook
Documentation of my Linux command-line journey.

## Environment

- **Local:** Fedora 43 (KDE Plasma)
- **Cloud practice:** Ubuntu 22.04 on AWS EC2

---

## Contents

- [Command Reference](#command-reference)
- [Challenges](#challenges)
- [Capstones](#capstones)
- [OverTheWire: Bandit](#overthewire-bandit)

---

## Command Reference

### File System & Navigation
| Command | Purpose | Example |
|---------|---------|---------|
| `pwd` | Print working directory | `pwd` |
| `ls -la` | List all files, long format | `ls -la /etc` |
| `cd` | Change directory | `cd /var/log` |
| `mkdir -p` | Create directory (and parents) | `mkdir -p dir/subdir` |
| `touch` | Create empty file | `touch file.txt` |
| `cp -r` | Copy recursively | `cp -r src/ dest/` |
| `mv` | Move or rename | `mv old.txt new.txt` |
| `rm -r` | Remove directory | `rm -r directory/` |
| `ln -s` | Create symbolic link | `ln -s target linkname` |
| `find` | Search for files | `find /etc -name "*.conf"` |
| `find -size` | Find by size | `find /var -size +10M` |
| `find -mmin` | Find by modified time | `find /etc -mmin -60` |
| `find -exec` | Run command on results | `find . -name "*.log" -exec rm {} \;` |

### Viewing Files
| Command | Purpose | Example |
|---------|---------|---------|
| `cat` | Print file contents | `cat config.txt` |
| `less` | Page through file | `less bigfile.log` |
| `head -n` | First N lines | `head -20 file.txt` |
| `tail -n` | Last N lines | `tail -50 file.txt` |
| `tail -f` | Follow file in real time | `tail -f /var/log/syslog` |

### Users, Groups & Permissions
| Command | Purpose | Example |
|---------|---------|---------|
| `whoami` | Current user | `whoami` |
| `id` | User ID and groups | `id username` |
| `useradd -m` | Create user with home dir | `sudo useradd -m alex` |
| `usermod -aG` | Add user to group | `sudo usermod -aG docker $USER` |
| `groupadd` | Create group | `sudo groupadd developers` |
| `passwd` | Set password | `sudo passwd alex` |
| `chmod` | Change permissions | `chmod 755 file` |
| `chown` | Change owner | `sudo chown user:group file` |
| `sudo` | Run as root | `sudo command` |

### Text Processing & Log Analysis
| Command | Purpose | Example |
|---------|---------|---------|
| `grep` | Search pattern in file | `grep "error" file.log` |
| `grep -i` | Case insensitive | `grep -i "error" file.log` |
| `grep -r` | Recursive search | `grep -r "localhost" /etc` |
| `grep -c` | Count matches | `grep -c "404" access.log` |
| `grep -v` | Exclude pattern | `grep -v "debug" file.log` |
| `grep -l` | Show filenames only | `grep -rl "error" /var/log` |
| `awk '{print $N}'` | Extract column N | `awk '{print $1}' file` |
| `sed 's/old/new/g'` | Find and replace | `sed 's/500/ERROR/g' file` |
| `sort` | Sort lines | `sort file.txt` |
| `uniq -c` | Count unique lines | `sort file \| uniq -c` |
| `wc -l` | Count lines | `wc -l file.txt` |
| `cut -d: -f1` | Extract field | `cut -d: -f1 /etc/passwd` |

### Process Management
| Command | Purpose | Example |
|---------|---------|---------|
| `ps aux` | All running processes | `ps aux` |
| `ps aux --sort=-%cpu` | Sort by CPU | `ps aux --sort=-%cpu \| head -6` |
| `top` | Real-time process viewer | `top` |
| `pgrep` | Find PID by name | `pgrep nginx` |
| `kill` | Send signal to PID | `kill 1234` |
| `kill -9` | Force kill | `kill -9 1234` |
| `killall` | Kill by name | `killall firefox` |
| `jobs` | List background jobs | `jobs` |
| `fg` | Bring job to foreground | `fg %1` |
| `bg` | Resume job in background | `bg %1` |
| `nohup ... &` | Run after logout | `nohup ./script.sh &` |
| `systemctl` | Manage services | `systemctl status nginx` |

### System Monitoring
| Command | Purpose | Example |
|---------|---------|---------|
| `uptime` | Load averages | `uptime` |
| `free -h` | Memory usage | `free -h` |
| `df -h` | Disk space by filesystem | `df -h` |
| `du -sh` | Directory size | `du -sh /var/*` |

### Networking
| Command | Purpose | Example |
|---------|---------|---------|
| `ip addr` | Show IP addresses | `ip addr show` |
| `ip route` | Show routing table | `ip route` |
| `ping -c 4` | Test connectivity | `ping -c 4 8.8.8.8` |
| `traceroute` | Trace network path | `traceroute google.com` |
| `ss -tuln` | Listening ports | `ss -tuln` |
| `ss -tulnp` | Listening ports + process | `sudo ss -tulnp` |
| `dig` | DNS lookup | `dig +short google.com` |
| `curl` | HTTP request | `curl -I https://example.com` |
| `wget` | Download file | `wget URL` |
| `nc -zv` | Test if port is open | `nc -zv host 80` |

### Package Management
| Task | Fedora (dnf) | Ubuntu (apt) |
|------|-------------|--------------|
| Update package lists | `sudo dnf check-update` | `sudo apt update` |
| Upgrade all packages | `sudo dnf upgrade` | `sudo apt upgrade` |
| Install package | `sudo dnf install pkg` | `sudo apt install pkg` |
| Remove package | `sudo dnf remove pkg` | `sudo apt remove pkg` |
| Search packages | `dnf search term` | `apt search term` |
| Package info | `dnf info pkg` | `apt show pkg` |
| List installed | `dnf list installed` | `apt list --installed` |
| Find package for file | `dnf provides */cmd` | `apt-file search cmd` |
| Remove unused deps | `sudo dnf autoremove` | `sudo apt autoremove` |
| Clean cache | `sudo dnf clean all` | `sudo apt clean` |

### Shell & Productivity
| Command | Purpose | Example |
|---------|---------|---------|
| `alias` | Create shortcut | `alias ll='ls -la'` |
| `export` | Set environment variable | `export EDITOR=vim` |
| `source` | Reload config file | `source ~/.bashrc` |
| `history` | Show command history | `history \| tail -20` |
| `!!` | Repeat last command | `sudo !!` |
| `Ctrl+R` | Search history | Type to search |
| `!$` | Last argument of prev command | `cat !$` |

---

## Challenges

| # | Topic | File |
|---|-------|------|
| 1 | File System Navigation & Manipulation | [challenges/1](challenges/1%20-%20File%20System%20Navigation%20%26%20Manipulation.md) |
| 2 | Users, Groups & Permissions | [challenges/2](challenges/2%20-%20Users%2C%20Groups%20%26%20Permissions.md) |
| 3 | Process Management & System Monitoring | [challenges/3](challenges/3%20-%20Process%20Management%20%26%20System%20Monitoring.md) |
| 4 | Log Analysis & Text Processing | [challenges/4](challenges/4%20-%20Log%20Analysis%20%26%20Text%20Processing.md) |
| 5 | Networking Basics | [challenges/5](challenges/5%20-%20Networking%20Basics.md) |
| 6 | Package Management | [challenges/6](challenges/6%20-%20Package%20Management.md) |
| 7 | Shell Customization & Productivity | [challenges/7](challenges/7%20-%20Shell%20Customization%20%26%20Productivity.md) |

---

## Capstones

[capstones/capstones.md](capstones/capstones.md)

---

## OverTheWire: Bandit

[OverTheWire/Bandit.md](OverTheWire/Bandit.md)