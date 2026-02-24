### Real-World Context

A well-configured shell makes you faster. Senior engineers invest time in shell configuration because productivity gains compound.

### Windows ↔ Linux Bridge

| Windows              | Linux              | Notes        |
| -------------------- | ------------------ | ------------ |
| PowerShell $PROFILE  | `~/.bashrc`        | Shell config |
| Environment Variables| `export VAR=value` | Set vars     |
| Aliases (doskey)     | `alias`            | Shortcuts    |
| PATH variable        | `$PATH`            | Command search|

### Core Commands Reference

| Command  | Purpose          | Example              |
| -------- | ---------------- | -------------------- |
| `alias`  | Create shortcut  | `alias ll='ls -la'`  |
| `export` | Set env variable | `export EDITOR=vim`  |
| `source` | Reload config    | `source ~/.bashrc`   |
| `history`| Show history     | `history`            |
| `!!`     | Repeat last      | `sudo !!`            |
| `Ctrl+R` | Search history   | Type to search       |

### Challenges:
---

**Challenge 7.1: Creating Aliases**

_Solution:_

```bash
alias ll='ls -la'
alias ..='cd ..'
alias grep='grep --color=auto'

# Make permanent:
echo "alias ll='ls -la'" >> ~/.bashrc
source ~/.bashrc
```

---

**Challenge 7.2: Modifying PATH**

_Solution:_

```bash
mkdir -p ~/bin
export PATH="$HOME/bin:$PATH"

# Make permanent:
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
```

---

**Challenge 7.3: Custom Prompt**

_Solution:_

```bash
# Green user@host, blue directory
PS1='\[\e[32m\]\u@\h\[\e[0m\]:\[\e[34m\]\w\[\e[0m\]\$ '
```

---

**Challenge 7.4: Shell Functions**

_Solution:_

```bash
# Create directory and cd into it
mkcd() { mkdir -p "$1" && cd "$1"; }

# Quick system status
status() {
    echo "Uptime: $(uptime -p)"
    echo "Memory: $(free -h | awk '/Mem/{print $3 "/" $2}')"
    echo "Disk: $(df -h / | awk 'NR==2{print $5}')"
}
```

---

**Challenge 7.5: History Mastery**

_Solution:_

```bash
history | tail -20
# Ctrl+R to search
!!                  # Repeat last command
sudo !!             # Repeat with sudo
!$                  # Last argument
```

---

**Challenge 7.6: Change to zsh SHELL**

_Solution:_

```bash
# Check if zsh is installed
which zsh

# If not installed (Fedora)
sudo dnf install zsh

# Change your default shell to zsh
chsh -s $(which zsh)

# Log out and back in for it to take effect
```

---