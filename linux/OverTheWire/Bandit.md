**Connection:** `ssh banditX@bandit.labs.overthewire.org -p 2220` (Replace X with your level number)

> **Note:** Passwords change periodically. The ones shown here may be outdated — use the password you actually receive from each level.

---

## Level 0 — SSH Login

**Challenge:** The goal of this level is for you to log into the game using SSH. The host to which you need to connect is bandit.labs.overthewire.org, on port 2220. The username is bandit0 and the password is bandit0. Once logged in, go to the Level 1 page to find out how to beat Level 1.

**Solution:**
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
# Password: bandit0
```
**Explanation:**
- `ssh` — Secure Shell, connects you to a remote machine
- `bandit0@` — the username you're logging in as
- `-p 2220` — specifies the port (default SSH is 22, but Bandit uses 2220)

---

## Level 0 → 1 — Read a File

**Challenge:** The password for the next level is stored in a file called `readme` located in the home directory. Use this password to log into bandit1 using SSH. Whenever you find a password for a level, use SSH (on port 2220) to log into that level and continue the game.

**Solution:**
```bash
ls          # See what files are here
cat readme  # Read the file

# Password: ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If
```
**Explanation:**
- `ls` — lists files in the current directory
- `cat` — prints the contents of a file to the screen

---

## Level 1 → 2 — Dashed filename

**Challenge:** The password for the next level is stored in a file called - located in the home directory

**Solution:**
```bash
cat ./-

# Password: 263JGJPfgU6LtdEvgfWU1XP5yac29mFx
```
**Explanation:**
- A filename starting with `-` confuses commands because `-` usually signals an option/flag
- `./-` tells the shell "this is a file path, not an option" — `./` means "in the current directory"

---

## Level 2 → 3 — Spaced filenames

**Challenge:** The password for the next level is stored in a file called --spaces in this filename-- located in the home directory

**Solution:**
```bash
cat "--spaces in this filename--"
# OR
cat ./--spaces\ in\ this\ filename--

# Password: MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx
```
**Explanation:**
- Spaces normally separate arguments in bash
- Wrapping in quotes treats the whole thing as one filename
- `--` tells `cat` to stop processing options
- Backslashes `\` escape each space individually
- *Tip:* Type `cat sp` then press *Tab* to auto-complete

---

## Level 3 → 4 — Hidden files

**Challenge:** The password for the next level is stored in a hidden file in the inhere directory.

**Solution:**
```bash
ls -la ./inhere/
#Output: -rw-r----- 1 bandit4 bandit3   33 Oct 14 09:26 ...Hiding-From-You

cat ./inhere/...Hiding-From-You

# Password: 2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ
```
**Explanation:**
- In Linux, files starting with `.` are hidden — `ls` won't show them by default
- `ls -a` (or `-la` for long format) reveals hidden files
---

## Level 4 → 5 — Human-Readable File

**Challenge:** The password for the next level is stored in the only human-readable file in the inhere directory. Tip: if your terminal is messed up, try the “reset” command.

**Solution:**
```bash
cd inhere
file ./*        # Check file types for all files
cat ./-file07   # The one that says "ASCII text"

# Password: 4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw
```
**Explanation:**
- `file` command identifies what type of data a file contains
- `./*` expands to all files in the current directory
- Most files will show "data" (binary); the password file shows "ASCII text"

---

## Level 5 → 6 — Find by File Properties

**Challenge:** The password for the next level is stored in a file somewhere under the inhere directory and has all of the following properties:
- human-readable
- 1033 bytes in size
- not executable

**Solution:**
```bash
du -a -b | grep 1033
#Output: 1033    ./inhere/maybehere07/.file2

cat inhere/maybehere07/.file2

# Password: HWasnPhtq9AVKe0dmk45nxy20cvUa6EG
```
**Explanation:**
- `find` searches recursively based on criteria
- `-size 1033c` — exactly 1033 bytes (`c` = bytes)
- `! -executable` — not executable
- `-exec file {} \;` — runs `file` on each match to check if it's human-readable

---

## Level 6 → 7 — Find Across the Server

**Challenge:** 
The password for the next level is stored somewhere on the server and has all of the following properties:
- owned by user bandit7
- owned by group bandit6
- 33 bytes in size

**Solution:**
```bash
cd /
find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null
# Output: cat /var/lib/dpkg/info/bandit7.password

cat /var/lib/dpkg/info/bandit7.password

# Password: morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj
```
**Explanation:**
- `find /` — search the entire filesystem from root
- `-user bandit7` — owned by user bandit7
- `-group bandit6` — owned by group bandit6
- `-size 33c` — exactly 33 bytes
- `2>/dev/null` — suppresses all the "Permission denied" errors

---

## Level 7 → 8 — Grep a Word

**Challenge:** The password for the next level is stored in the file data.txt next to the word millionth

**Solution:**
```bash
grep "millionth" data.txt

# Password: dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc
```
**Explanation:**
- `grep` searches for a text pattern inside a file
- Returns the entire line containing the match
- The password is the second field on that line
  
---

## Level 8 → 9 — Find Unique Line

**Challenge:** The password for the next level is stored in the file data.txt and is the only line of text that occurs only once

**Solution:**
```bash
sort data.txt | uniq -u

# Password: 4CKMh1JI91bUIZZPXDqGanal4xvAg0JM
```
**Explanation:**
- `sort` — arranges lines alphabetically (required because `uniq` only detects _adjacent_ duplicates)
- `uniq -u` — prints only lines that appear exactly once
- The pipe `|` sends output of `sort` into `uniq`

---

## Level 9 → 10 — Strings in Binary

**Challenge:** The password for the next level is stored in the file data.txt in one of the few human-readable strings, preceded by several ‘=’ characters.

**Solution:**
```bash
strings data.txt | grep "=="

# Password: FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey
```
**Explanation:**
- `strings` — extracts printable text from binary files
- `grep "=="` — filters for lines containing `==`, which precede the password
---

## Level 10 → 11 — Base64 Decode

**Challenge:** The password for the next level is stored in the file data.txt, which contains base64 encoded data

**Solution:**
```bash
base64 -d data.txt

# Password: dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr
```
**Explanation:**
- `base64` encodes/decodes data in Base64 format
- `-d` flag means decode
- Base64 is commonly used for encoding binary data as text (e.g. email attachments, API tokens)
---

## Level 11 → 12 — ROT13

**Challenge:** The password for the next level is stored in the file data.txt, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions

**Solution:**
```bash
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'

# Password: 7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4
```
**Explanation:**
- `tr` translates (replaces) characters
- ROT13 shifts each letter 13 places in the alphabet (A→N, B→O, etc.)
- `'A-Za-z'` is the input range, `'N-ZA-Mn-za-m'` is the shifted range
- Applying ROT13 twice returns the original text
---

## Level 12 → 13 — Repeated Decompression

**Challenge:** The password for the next level is stored in the file data.txt, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under /tmp in which you can work. Use mkdir with a hard to guess directory name. Or better, use the command “mktemp -d”. Then copy the datafile using cp, and rename it using mv (read the manpages!)

**Solution:**
```bash
cd /
cd $(mktemp -d) # Create temporary directory and change into it.
vim decompress.sh # Paste below script into file
```
```bash
#!/bin/bash
set -e

# Clean up on exit (success or failure)
cleanup() {
    rm -f hexdump_data compressed_data* data5.bin data6.bin data8 data8.gz
}
trap cleanup EXIT

cp ~/data.txt .
mv data.txt hexdump_data

echo "[1/8] Reversing hex dump..."
xxd -r hexdump_data compressed_data

echo "[2/8] Decompressing gzip..."
mv compressed_data compressed_data.gz
gzip -d compressed_data.gz

echo "[3/8] Decompressing bzip2..."
mv compressed_data compressed_data.bz2
bzip2 -d compressed_data.bz2

echo "[4/8] Extracting tar..."
mv compressed_data compressed_data.tar
tar -xf compressed_data.tar

echo "[5/8] Extracting tar (data5.bin)..."
tar -xf data5.bin

echo "[6/8] Extracting tar (data6.bin)..."
tar -xf data6.bin

echo "[7/8] Decompressing gzip (data8.bin)..."
mv data8.bin data8.gz
gzip -d data8.gz

echo "[8/8] Done!"
cat data8

# ======================================== END OF SCRIPT ========================================
```
```bash
:wq! # Save and exit from VIM editor
chmod +x decompress.sh && ./decompress.sh

# Password: FO5dwFsc0cbaIiH0h8J2eUks2vdTDwAn
```
**Explanation:**
- `set -e` exits the script immediately if any command fails, prevents running on broken data
- `trap cleanup EXIT` runs the cleanup function automatically when the script ends, whether it succeeds or fails
- `xxd -r` reverses a hex dump back to binary
- `gzip -d` decompresses a .gz file
- `bzip2 -d` decompresses a .bz2 file
- `tar -xf` extracts files from a tar archive (x = extract, f = from file)
---

## Level 13 → 14 — SSH with Private Key

**Challenge:** The password for the next level is stored in /etc/bandit_pass/bandit14 and can only be read by user bandit14. For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level. Look at the commands that logged you into previous bandit levels, and find out how to use the key for this level.



**Solution:**
```bash
scp -P 2220 bandit13@bandit.labs.overthewire.org:sshkey.private .
chmod 600 sshkey.private
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220

```
**Explanation:**
- `ssh -i` — specifies an identity file (private key) instead of a password
- `localhost` — connects to the same machine you're already on
- SSH keys are the standard way to authenticate in real-world DevOps (more secure than passwords)
- Once logged in as bandit14, you can read the password file
---

## Level 14 → 15 — Send Data Over the Network

**Challenge:** The password for the next level can be retrieved by submitting the password of the current level to port 30000 on localhost.

**Solution:**
```bash
cat /etc/bandit_pass/bandit14 # Retrieve current password
#Output: MU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS

echo "MU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS" | nc localhost 30000
#Output: 8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo
```
**Explanation:**
-  `nc` (netcat) — a tool for reading/writing data across network connections
- `localhost` — refers to the machine you're already on (127.0.0.1)
- `30000` — the port number to connect to
- The pipe `|` sends the password as input to the nc connection
- The server on port 30000 checks the password and returns the next one
---

## Level 15 → 16 — SSL/TLS Encrypted Connection

**Challenge:** The password for the next level can be retrieved by submitting the password of the current level to port 30001 on localhost using SSL/TLS encryption.

Helpful note: Getting “DONE”, “RENEGOTIATING” or “KEYUPDATE”? Read the “CONNECTED COMMANDS” section in the manpage.

**Solution:**
```bash
echo "8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo" | openssl s_client -quiet -connect localhost:30001
# Password: kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx
```
**Explanation:**
- `openssl s_client` — connects to a server using SSL/TLS encryption
- `-quiet` — suppresses the certificate info and handshake output, showing only the response
- `-connect localhost:30001` — specifies host and port
- This is the same concept as Level 14→15, but encrypted — `nc` won't work because the server requires SSL

**Why this matters:** In the real world, services like HTTPS (port 443) use SSL/TLS. You'll use `openssl s_client` to debug SSL certificate issues on web servers.

---

## Level 16 → 17 — Port Scanning with Nmap

**Challenge:** The credentials for the next level can be retrieved by submitting the password of the current level to a port on localhost in the range 31000 to 32000. First find out which of these ports have a server listening on them. Then find out which of those speak SSL/TLS and which don’t. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.

Helpful note: Getting “DONE”, “RENEGOTIATING” or “KEYUPDATE”? Read the “CONNECTED COMMANDS” section in the manpage.

**Solution:**
```bash
# Step 1: Scan ports to find open ones and their services
nmap -sV -p 31000-32000 localhost

# Step 2: You'll see ~5 open ports. Most run "echo" (they just repeat your input)
# Find the one running SSL that ISN'T echo (likely port 31790)

# Step 3: Submit the password via SSL
echo "kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx" | openssl s_client -quiet -connect localhost:31790

# Step 4: You'll receive an RSA private key (not a password this time)
# Save it to a file
cd $(mktemp -d)
vim sshkey17.private   # Paste the entire key including BEGIN/END lines

# Step 5: Set correct permissions (SSH requires this)
chmod 600 sshkey17.private

# Step 6: Use the key to log into the next level
ssh -i sshkey17.private bandit17@bandit.labs.overthewire.org -p 2220
```
**Explanation:**
- `nmap` — network scanner that discovers open ports and services
- `-sV` — detect what service/version is running on each port
- `-p 31000-32000` — only scan this port range
- `chmod 600` — SSH refuses to use a private key if other users can read it
- The echo ports just mirror your input back — you need the one that actually processes it

---

## Level 17 → 18 — Find the Difference

**Challenge:** 

**Solution:**
```bash
diff passwords.old passwords.new
# Output:   < x2gLTTjFwMOhQ8oWNbMN362QKxfRqGlO

```
**Explanation:**
- `diff` — compares two files line by line and shows what's different
- Output format: `<` means the line is from the first file, `>` means it's from the second file
- The `>` line from `passwords.new` is your password

**Why this matters:** `diff` is used constantly in DevOps — comparing config files, checking what changed in deployments, reviewing code changes. It's the foundation of how `git diff` works.
---

## Level 18 → 19 — Bypassing .bashrc Logout

**Challenge:** The password for the next level is stored in a file `readme` in the homedirectory. Unfortunately, someone has modified `.bashrc` to log you out when you log in with SSH.

**Solution:**
```bash
# Option 1: Execute a command directly via SSH (runs before .bashrc kicks you out)
ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme

# Option 2: Start a shell that skips .bashrc
ssh -t bandit18@bandit.labs.overthewire.org -p 2220 "bash --norc --noprofile"
# Then: cat readme

# Password: cGWpMaKXVwDUNgPAVJbWYuGHVn9zl3j8
```
**Explanation:**
- `ssh user@host command` — runs a single command on the remote machine without starting an interactive shell
- `.bashrc` runs when an interactive bash session starts — bypassing it avoids the logout trap
- `-t` — forces a pseudo-terminal allocation (needed for interactive shell)
- `--norc` — tells bash not to read `.bashrc`
- `--noprofile` — tells bash not to read `.bash_profile`
---

**Why this matters:** Understanding shell startup files (`.bashrc`, `.bash_profile`, `.profile`) is important. A broken `.bashrc` can lock you out of a server — knowing how to bypass it is a real recovery skill.

## Level 19 → 20 — SetUID Binary

**Challenge:** To gain access to the next level, you should use the setuid binary in the homedirectory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (/etc/bandit_pass), after you have used the setuid binary.

**Solution:**
```bash
ls -la                    # See the bandit20-do file
./bandit20-do             # Run it without args to see usage
./bandit20-do id          # Test - shows you're running as bandit20
# Output: uid=11019(bandit19) gid=11019(bandit19) euid=11020(bandit20) groups=11019(bandit19)

./bandit20-do cat /etc/bandit_pass/bandit20

# Password: 0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO
```
**Explanation:**
- _SetUID (Set User ID)_ — when a file has the setuid bit set, it runs with the permissions of the file's **owner**, not the user executing it
- `ls -la` shows `-rwsr-x---` — the `s` in the owner's execute position means setuid is enabled
- `bandit20-do` is owned by bandit20, so anything you run through it executes as bandit20
- This lets you read `/etc/bandit_pass/bandit20` which only bandit20 can access


**Why this matters:** SetUID is a key Linux security concept. Misconfigured setuid binaries are a common privilege escalation vulnerability. Commands like `passwd` and `sudo` use setuid to let regular users perform privileged operations safely.

---

## Level 20 → 21 — SetUID + Netcat Listener

**Challenge:** There is a setuid binary in the homedirectory that does the following: it makes a connection to localhost on the port you specify as a commandline argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).

NOTE: Try connecting to your own network daemon to see if it works as you think

**Solution:**
```bash
echo "$(cat /etc/bandit_pass/bandit20)" | nc -l -p 4444 & 

./suconnect 4444

# Password: EeoULMCra2q0dSkYj561DX7s1CpBuOBt
```
**Explanation:** 
- `nc -l -p 4444` — starts netcat as a **listener** on port 4444 (waits for incoming connections)
- `echo "password" |` — pipes the password to netcat so it sends it when something connects
- `&` — runs the listener in the background so you can use the same terminal
- `./suconnect 4444` — the setuid binary connects to port 4444, reads the password, verifies it, and sends back the next password
- The `&` trick avoids needing two separate SSH sessions

**Why this matters:** This combines networking (`nc`), background processes (`&`), and setuid concepts. Setting up listeners and connecting services together is common in DevOps troubleshooting and security testing.

---