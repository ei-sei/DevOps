### Real-World Context

Linux security is built on users, groups, and permissions. You'll manage:
- Service accounts for applications
- Team access to shared directories
- Security hardening of configuration files

### Windows ↔ Linux Bridge

| Windows                | Linux                       | Notes                |
| ---------------------- | --------------------------- | -------------------- |
| Local Users and Groups | `/etc/passwd`, `/etc/group` | User/group databases |
| Administrator          | root (UID 0)                | Superuser account    |
| "Run as administrator" | `sudo`                      | Elevate privileges   |
| NTFS permissions       | rwx permissions             | Similar concept      |

### Understanding Permission Strings

```
-rwxr-xr--
│├─┤├─┤├─┤
│ │  │  └── Others: r-- (read only)
│ │  └───── Group:  r-x (read and execute)
│ └──────── Owner:  rwx (read, write, execute)
└────────── Type: - (file), d (dir), l (link)
```

**Numeric permissions:** r=4, w=2, x=1

|Numeric|Symbolic|Use Case|
|---|---|---|
|755|rwxr-xr-x|Executables, directories|
|644|rw-r--r--|Regular files|
|700|rwx------|Private directories|
|600|rw-------|Private files, SSH keys|

### Core Commands Reference

|Command|Purpose|Example|
|---|---|---|
|`whoami`|Show current user|`whoami`|
|`id`|Show user ID and groups|`id username`|
|`useradd`|Create user|`sudo useradd -m username`|
|`usermod`|Modify user|`sudo usermod -aG group user`|
|`groupadd`|Create group|`sudo groupadd groupname`|
|`passwd`|Set password|`sudo passwd username`|
|`chown`|Change owner|`sudo chown user:group file`|
|`chmod`|Change permissions|`chmod 755 file`|
|`sudo`|Run as root|`sudo command`|

### Challenges:
---
 
**Challenge 2.1: User Reconnaissance**

_Task:_ Determine your username, user ID, and group memberships.

_Solution:_
```bash
whoami
id
groups
sudo whoami    # Test sudo access
```

---

**Challenge 2.2: Creating a New User**

_Task:_ Create user "alex" with home directory and set password.

_Solution:_
```bash
sudo useradd -m alex
sudo passwd alex
grep alex /etc/passwd
```
Create a new user named alex with a home directory, set their password, and verify that the user was created by checking the system’s user database.

---

**Challenge 2.3: Working with Groups**

_Task:_ Create "developers" group and add users to it. (Groups are used to share permissions (files, directories, access))

_Solution:_

```bash
sudo groupadd developers
sudo usermod -aG developers alex
sudo usermod -aG developers $USER   # Adds current logged in user to developers group
groups alex
```

⚠️ **Warning:** Never forget the `-a` flag! Without it, you REPLACE all groups!

---

**Challenge 2.4: Changing Permissions**

_Task:_ Create a script with owner rwx, group r-x, others nothing (750).

_Solution:_

```bash
echo '#!/bin/bash' > myscript.sh
echo 'echo "Hello"' >> myscript.sh
chmod 750 myscript.sh
ls -l myscript.sh
```

---

**Challenge 2.5: Shared Directory Setup**

_Task:_ Create `/tmp/shared-project` where developers can collaborate and new files inherit group ownership.

_Solution:_

```bash
sudo mkdir /tmp/shared-project
sudo chown root:developers /tmp/shared-project
sudo chmod 2775 /tmp/shared-project
# 2 = setgid bit (files inherit group)
ls -ld /tmp/shared-project
# Should show: drwxrwsr-x
```

---

