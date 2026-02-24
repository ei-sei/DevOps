### Real-World Context

Package management is how you install, update, and remove software. Unlike Windows where you download individual installers, Linux uses package managers that handle dependencies automatically.

**Key insight for DevOps:** You'll encounter both `dnf` (Fedora/RHEL/CentOS) and `apt` (Ubuntu/Debian) in your career. Knowing both is valuable since enterprises often use RHEL-based systems while cloud instances commonly run Ubuntu.

### Windows ↔ Linux Bridge

| Windows              | Linux (Fedora)       | Linux (Ubuntu)        |
| -------------------- | -------------------- | --------------------- |
| Programs & Features  | `dnf list installed` | `apt list --installed`|
| Download installer   | `dnf install pkg`    | `apt install pkg`     |
| Windows Update       | `dnf upgrade`        | `apt upgrade`         |

### Core Commands Reference (Fedora - dnf)

| Command              | Purpose                  | Example                   |
| -------------------- | ------------------------ | ------------------------- |
| `dnf check-update`   | Check for updates        | `sudo dnf check-update`   |
| `dnf upgrade`        | Upgrade all packages     | `sudo dnf upgrade`        |
| `dnf install`        | Install package          | `sudo dnf install nginx`  |
| `dnf remove`         | Remove package           | `sudo dnf remove nginx`   |
| `dnf search`         | Search packages          | `dnf search nginx`        |
| `dnf info`           | Package details          | `dnf info nginx`          |
| `dnf list installed` | List installed           | `dnf list installed`      |
| `dnf autoremove`     | Remove unused            | `sudo dnf autoremove`     |
| `dnf provides`       | Find what provides a file| `dnf provides */bin/tree`  |

### Comparison: dnf vs apt

| Task                 | Fedora (dnf)             | Ubuntu (apt)            |
| -------------------- | ------------------------ | ----------------------- |
| Update package lists | `sudo dnf check-update`  | `sudo apt update`       |
| Upgrade all packages | `sudo dnf upgrade`       | `sudo apt upgrade`      |
| Install package      | `sudo dnf install pkg`   | `sudo apt install pkg`  |
| Remove package       | `sudo dnf remove pkg`    | `sudo apt remove pkg`   |
| Search packages      | `dnf search term`        | `apt search term`       |
| Package info         | `dnf info pkg`           | `apt show pkg`          |
| Find package for file| `dnf provides */cmd`     | `apt-file search cmd`   |
| Clean cache          | `sudo dnf clean all`     | `sudo apt clean`        |
| Remove unused        | `sudo dnf autoremove`    | `sudo apt autoremove`   |

### Challenges:
---

**Challenge 6.1: Update Your System**

_Solution:_
```bash
# Check what updates are available
sudo dnf check-update

# Upgrade all packages
sudo dnf upgrade -y

# For Ubuntu servers you'll manage:
# sudo apt update && sudo apt upgrade -y
```

---

**Challenge 6.2: Search and Install Packages**

_Solution:_
```bash
# Search for a package
dnf search tree

# Get package info
dnf info tree

# Install the package
sudo dnf install tree

# Verify installation
which tree
tree --version
```

---

**Challenge 6.3: Find What Provides a Command**

_Task:_ You need a command that isn't installed. Find which package provides it.

_Solution:_
```bash
# Find which package provides a command
dnf provides */bin/htop

# Or for any file
dnf provides */traceroute

# Then install it
sudo dnf install htop
```

---

**Challenge 6.4: List and Clean Up Packages**

_Solution:_
```bash
# Count installed packages
dnf list installed | wc -l

# List recently installed
dnf history list

# Remove unused dependencies
sudo dnf autoremove

# Clean package cache
sudo dnf clean all
```

---

**Challenge 6.5: Working with Package Groups**

_Fedora feature:_ Install related packages as a group.

_Solution:_
```bash
# List available groups
dnf group list

# See what's in a group
dnf group info "Development Tools"

# Install a group
sudo dnf group install "Development Tools"
```

---
