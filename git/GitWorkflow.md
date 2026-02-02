# Git Version Control – Final Lab Notebook

This document is a consolidated and cleaned-up **final Markdown version** combining the content of **Git.md** and the practical exercises demonstrated in **Git_Excercise--git_init_branch_merge_delete.pdf**. It serves as a complete, end-to-end Git fundamentals and branching workflow lab.

---

## Environment

* **Local OS:** Fedora (KDE Plasma)
* **Editor:** Nano
* **Remote Platform:** GitHub
* **Authentication:** Personal Access Token (PAT)

---

## 1. Repository Initialization

### Create a project directory

```bash
mkdir Devops_bootcamp
cd Devops_bootcamp
```

### Initialize a Git repository

```bash
git init
```

Verify repository status:

```bash
git status
```

---

## 2. File Creation and First Commit

### Create a file

```bash
touch git_ex.txt
```

### Edit file and add shebang

```bash
nano git_ex.txt
```

Add the following line:

```bash
#!/bin/bash
```

Save and exit (`Ctrl+O`, `Ctrl+X`).

### Stage and commit the file

```bash
git add git_ex.txt
git commit -m "This is the first commit"
```

---

## 3. Rename File and Update Permissions

### Rename file to a bash script

```bash
mv git_ex.txt git_ex.sh
```

### Make script executable

```bash
chmod 744 git_ex.sh
```

### Stage and commit changes

```bash
git add git_ex.sh
git commit -m "Change file extension to .sh"
```

---

## 4. Viewing Commit History

```bash
git log
```

This command displays:

* Commit hashes
* Author information
* Commit messages
* Timestamps

---

## 5. Creating a Remote Repository (GitHub)

### Option A: Create repository via GitHub UI

1. Log in to GitHub
2. Click **New Repository**
3. Name the repository
4. Select Public or Private

### Option B: Create repository using GitHub API

```bash
curl -u "USERNAME" https://api.github.com/user/repos -d '{"name":"Dev_repo"}'
```

> Authentication requires a **Personal Access Token (PAT)** instead of a password.

---

## 6. Connect Local Repo to Remote

```bash
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git remote -v
```

### Push local repository

```bash
git push -u origin main
```

---

## 7. Updating Files and Pushing Changes

### Create files

```bash
touch names.txt names2.txt
```

### Edit file content

```bash
nano names.txt
```

Add names of two animals and save.

### Stage, commit, and push

```bash
git add .
git commit -m "Added the names of 2 animals"
git push
```

---

## 8. Branching and Feature Development

### Create a feature branch

```bash
git branch feature/dev
git switch feature/dev
```

### Create a new feature file

```bash
touch features.txt
```

### Rename file and create a script

```bash
mv features.txt features.sh
nano features.sh
```

Example script:

```bash
#!/bin/bash
count=1
while [ $count -le 5 ]
do
  echo "Hello World"
  count=$((count+1))
done
```

### Make script executable

```bash
chmod 744 features.sh
```

### Stage, commit, and push branch

```bash
git add .
git commit -m "Add shell script"
git push --set-upstream origin feature/dev
```

---

## 9. Merging and Branch Cleanup

### Switch back to main branch

```bash
git switch main
```

### Merge feature branch

```bash
git merge feature/dev
```

### Delete feature branch

```bash
git branch -d feature/dev
git push
```

---

## 10. Authentication Troubleshooting

### GitHub Password Authentication Error

```
remote: Support for password authentication was removed
fatal: Authentication failed
```

### Solution: Use a Personal Access Token (PAT)

1. GitHub → Settings
2. Developer Settings
3. Personal Access Tokens
4. Generate new token
5. Use token as password when prompted

---

## Summary of Commands

| Task            | Command                   |
| --------------- | ------------------------- |
| Initialize repo | `git init`                |
| Stage files     | `git add .`               |
| Commit changes  | `git commit -m "message"` |
| View history    | `git log`                 |
| Create branch   | `git branch <name>`       |
| Switch branch   | `git switch <name>`       |
| Merge branch    | `git merge <branch>`      |
| Delete branch   | `git branch -d <branch>`  |
| Push to remote  | `git push`                |

---

## Notes

This lab demonstrates:

* Git fundamentals
* Remote repository management
* PAT authentication
* Branching and merging workflows
* Basic shell scripting within Git workflows

**Status:** Complete foundational Git lab
