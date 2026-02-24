### Real-World Context

As a DevOps engineer, you'll navigate servers via command line constantly. You'll need to:

- Find configuration files buried in directory structures
- Locate log files consuming disk space
- Deploy application code to correct directories
- Clean up old files during incident response

### Windows ↔ Linux Bridge

| Windows | Linux | Notes |
|---------|-------|-------|
| `C:\Users\You` | `/home/you` | Home directory |
| `C:\` | `/` | Root of filesystem |
| `dir` | `ls` | List directory contents |
| `cd` | `cd` | Change directory (same!) |
| `copy` | `cp` | Copy files |
| `move` | `mv` | Move/rename files |
| `del` | `rm` | Delete files |
| `mkdir` | `mkdir` | Create directory (same!) |
| `type` | `cat` | Display file contents |
| Explorer search | `find`, `locate` | Search for files |

### Core Commands Reference

| Command | Purpose | Example |
| ------- | ------------------------ | --------------------------------- |
| `pwd` | Print working directory | `pwd` → `/home/you` |
| `ls` | List directory contents | `ls -la` (all files, long format) |
| `cd` | Change directory | `cd /var/log` |
| `mkdir` | Create directory | `mkdir -p dir/subdir` |
| `touch` | Create empty file | `touch newfile.txt` |
| `cp` | Copy files/directories | `cp -r source/ dest/` |
| `mv` | Move or rename | `mv old.txt new.txt` |
| `rm` | Remove files/directories | `rm -r directory/` |
| `find` | Search for files | `find /path -name "*.log"` |
| `grep` | Search inside files | `grep "error" file.txt` |
| `cat` | Display file contents | `cat config.txt` |
| `less` | Page through file | `less bigfile.log` |
| `head` | Show first lines | `head -20 file.txt` |
| `tail` | Show last lines | `tail -50 file.txt` |
| `ln` | Create links | `ln -s target linkname` |

  
### Challenges:
---
 
**Challenge 1.1: Basic Navigation**

_Task:_
You've SSH'd into a new server. Orient yourself.

1. Confirm your current location

2. List all files including hidden ones

3. Navigate to the system log directory

4. Return home using shortest command

_Solution:_

```bash
pwd # Where am I?

ls -la # List everything

cd /var/log # Go to logs

cd # Return home (shortest!)

```

---

**Challenge 1.2: Creating Project Structure**

_Task:_
Create the following standard project directory structure with one command `project/{src,docs,tests,config}`

_Solution:_
```bash
mkdir -p project/{src,docs,tests,config}
ls project/
```

-p -> "parents: This creates a parent directory if they don't exist and does not error if a directory already exists

{} brace expansion handled by shell allows you to create subdirectories of project

---

**Challenge 1.3: Finding Files by Name**

_Task:_
Find all files in `/etc` containing "nginx" in their name.

_Solution:_
```bash
find /etc -name "*nginx*" 2>/dev/null

# Case-insensitive:
find /etc -iname "*nginx*" 2>/dev/null
```

Breakdown:
- find
	The command used to search for files and directories.

- /etc
	The starting directory for the search. find will recursively scan everything under /etc.

- -name "*nginx*"
	-name → match by filename (case-sensitive)
	*→ wildcard pattern:
	* means “anything”
	so this matches names like:
		nginx.conf
		nginx-sites
		my-nginx-backup

- 2>/dev/null
	Redirects stderr (error output) to /dev/null (the “black hole”).

---

**Challenge 1.4: Finding Large Files**

_Task:_
Find files larger than 10MB in `/var`.

_Solution:_
```bash

sudo find /var -size +10M 2>/dev/null

# With sizes:
sudo find /var -size +10M -exec ls -lh {} \; 2>/dev/null
```
`2>/dev/null` silences error messages by sending them to a "black hole" so only useful output shows on screen.

---

**Challenge 1.5: Finding Recently Modified Files**

_Task:_
Find `.conf` files in `/etc` modified in last 60 minutes.

_Solution:_
```bash
sudo find /etc -name "*.conf" -mmin -60 2>/dev/null

# Modified in last 24 hours:
sudo find /etc -name "*.conf" -mtime -1 2>/dev/null
```

---

**Challenge 1.6: Searching Inside Files**

_Task:_
Search all files in `/etc` for "localhost".

_Solution:_
```bash
sudo grep -r "localhost" /etc 2>/dev/null

# Show only filenames:
sudo grep -rl "localhost" /etc 2>/dev/null
```

---

**Challenge 1.7: Symbolic Links**

_Task:_
A **symbolic link** is a special file that **points to another file or directory**.
Create a link so `/tmp/myapp/config.yml` points to `~/configs/myapp.yml`.

_Solution:_
```bash
mkdir -p ~/configs

echo "database: production" > ~/configs/myapp.yml

mkdir -p /tmp/myapp

# Create symbolic link
ln -s ~/configs/myapp.yml /tmp/myapp/config.yml

# Verify
ls -la /tmp/myapp/

cat /tmp/myapp/config.yml
```

---