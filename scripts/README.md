# DevOps

A collection of Bash automation scripts and reference documentation for system administration and DevOps tasks.

## Scripts

| Script | Description |
|--------|-------------|
| [system-health-check.sh](Bash/system-health-check.sh) | Monitors CPU, memory, and disk usage with configurable thresholds, color output, and logging |
| [calculator.sh](Bash/calculator.sh) | Prompts for two numbers and performs addition, subtraction, multiplication, and division |
| [fileOperations.sh](Bash/fileOperations.sh) | Creates a directory and writes a timestamped message to a file |
| [fileChecker.sh](Bash/fileChecker.sh) | Checks if a file exists and reports its read, write, and execute permissions |
| [backupTextFiles.sh](Bash/backupTextFiles.sh) | Copies all .txt files from a source directory into a timestamped backup directory |
| [systemMonitor.sh](Bash/systemMonitor.sh) | Displays a system report covering CPU, memory, disk usage, and top processes, saved to a log file |

### Quick Start

```bash
# Make all scripts executable
chmod +x Bash/*.sh

# Run the system monitor
./Bash/systemMonitor.sh

# Run the calculator
./Bash/calculator.sh

# Check file permissions
./Bash/fileChecker.sh

# Backup text files
./Bash/backupTextFiles.sh

# Run a health check with default thresholds
./Bash/system-health-check.sh
```

## Documentation

- [Bash Scripting Fundamentals](docs/Index.md) — A practical guide covering Bash from basics to real-world patterns
- [Production-Quality Script Standards](docs/Production-Quality-Script-Standards.md) — Guidelines for writing scripts ready for real use
