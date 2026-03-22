# Git Lab Notebook

Documentation of Git version control fundamentals, branching workflows, and authentication.



## Contents


- [Git Lab Notebook](#git-lab-notebook)
  - [Contents](#contents)
  - [Git Cheatsheet](#git-cheatsheet)
  - [Repository Initialisation](#repository-initialisation)
  - [File Creation and First Commit](#file-creation-and-first-commit)
  - [Rename File and Update Permissions](#rename-file-and-update-permissions)
  - [Viewing Commit History](#viewing-commit-history)
  - [Creating a Remote Repository (GitHub)](#creating-a-remote-repository-github)
    - [Via GitHub UI](#via-github-ui)
    - [Via GitHub API](#via-github-api)
  - [Connect Local Repo to Remote](#connect-local-repo-to-remote)
  - [Updating Files and Pushing Changes](#updating-files-and-pushing-changes)
  - [Branching and Feature Development](#branching-and-feature-development)
  - [Merging and Branch Cleanup](#merging-and-branch-cleanup)
  - [Authentication Troubleshooting](#authentication-troubleshooting)
    - [GitHub Password Authentication Error](#github-password-authentication-error)
    - [Solution: Use a Personal Access Token (PAT)](#solution-use-a-personal-access-token-pat)
  - [Command Reference](#command-reference)

---

## Git Cheatsheet

![git cheatsheet](/git-cheatsheet.png)

---

## Repository Initialisation

```bash
mkdir Devops_project
cd Devops_project
git init
git status
```

---

## File Creation and First Commit

```bash
touch git_ex.txt
nano git_ex.txt
```

Add the following line:

```bash
#!/bin/bash
```

Stage and commit:

```bash
git add git_ex.txt
git commit -m "This is the first commit"
```

---

## Rename File and Update Permissions

```bash
mv git_ex.txt git_ex.sh
chmod 744 git_ex.sh
git add git_ex.sh
git commit -m "Change file extension to .sh"
```

---

## Viewing Commit History

```bash
git log
```

Displays commit hashes, author info, messages, and timestamps.

---

## Creating a Remote Repository (GitHub)

### Via GitHub UI

1. Log in to GitHub
2. Click **New Repository**
3. Name the repository
4. Select Public or Private

### Via GitHub API

```bash
curl -u "USERNAME" https://api.github.com/user/repos -d '{"name":"Dev_repo"}'
```

> Authentication requires a **Personal Access Token (PAT)** instead of a password.

---

## Connect Local Repo to Remote

```bash
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git remote -v
git push -u origin main
```

---

## Updating Files and Pushing Changes

```bash
touch names.txt names2.txt
nano names.txt
git add .
git commit -m "Added the names of 2 animals"
git push
```

---

## Branching and Feature Development

```bash
git branch feature/dev
git switch feature/dev
touch features.txt
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

```bash
chmod 744 features.sh
git add .
git commit -m "Add shell script"
git push --set-upstream origin feature/dev
```

---

## Merging and Branch Cleanup

```bash
git switch main
git merge feature/dev
git branch -d feature/dev
git push
```

---

## Authentication Troubleshooting

### GitHub Password Authentication Error

```
remote: Support for password authentication was removed
fatal: Authentication failed
```

### Solution: Use a Personal Access Token (PAT)

1. GitHub > Settings
2. Developer Settings
3. Personal Access Tokens
4. Generate new token
5. Use token as password when prompted

---

## Command Reference

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
