# Automation Scripts

A collection of Bash automation scripts and reference documentation for system administration and DevOps tasks.

## Scripts

| Script | Description |
|--------|-------------|
| [calculator.sh](scripts/calculator.sh) | Prompts for two numbers and performs addition, subtraction, multiplication, and division |
| [fileOperations.sh](scripts/fileOperations.sh) | Creates a directory and writes a timestamped message to a file |
| [fileChecker.sh](scripts/fileChecker.sh) | Checks if a file exists and reports its read, write, and execute permissions |
| [backupTextFiles.sh](scripts/backupTextFiles.sh) | Copies all .txt files from a source directory into a timestamped backup directory |
| [systemMonitor.sh](scripts/systemMonitor.sh) | Displays a system report covering CPU, memory, disk usage, and top processes, saved to a log file |
| [bashBattleArena.sh](scripts/bashBattleArena.sh) | Practice exercise covering directory creation, file operations, and basic commands |

### Quick Start

```bash
# Make all scripts executable
chmod +x scripts/*.sh

# Run the calculator
./scripts/calculator.sh

# Run the system monitor
./scripts/systemMonitor.sh

# Check file permissions
./scripts/fileChecker.sh

# Backup text files
./scripts/backupTextFiles.sh
```

## Bash Scripting Fundamentals

A practical guide to writing Bash scripts, starting from the basics and building up to patterns you'll use in real scripts.

| # | Topic | Concept |
|---|-------|---------|
| 1 | [Variables & Parameters](notes/01-Variables-and-Parameters.md) | Storing data, arrays, passing arguments, string manipulation |
| 2 | [Conditionals, Loops & Flow Control](notes/02-Conditionals-Loops-and-Flow-Control.md) | Making decisions, repeating actions, case statements, menus |
| 3 | [Functions & Inputs](notes/03-Functions-and-Inputs.md) | Reusable code blocks, argument parsing with flags |
| 4 | [Piping & Redirection](notes/04-Piping-and-Redirection.md) | Connecting commands, file descriptors, here-documents |
| 5 | [Error Handling & Exit Codes](notes/05-Error-Handling-and-Exit-Codes.md) | Exit codes, safety options, traps, debugging |
| 6 | [Common Patterns & Utilities](notes/06-Common-Patterns-and-Utilities.md) | Logging, retry logic, text tools, lock files |

See also: [Production-Quality Script Standards](notes/07-Production-Quality-Script-Standards.md)
