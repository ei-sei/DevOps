#!/bin/bash

# Displays a system report covering CPU usage, memory, disk usage, and the top
# 5 processes by memory. Saves the output to a timestamped log file.

TIMESTAMP=$(date +%Y-%m-%d_%H:%M:%S)
LOG_FILE="system_monitor_$TIMESTAMP.log"

{
    echo "=== System Monitor Report: $TIMESTAMP ==="
    echo ""

    echo "--- CPU Usage ---"
    top -bn1 | grep "%Cpu"
    echo ""

    echo "--- Memory Usage ---"
    free -h
    echo ""

    echo "--- Disk Usage ---"
    df -h
    echo ""

    echo "--- Top 5 Processes by Memory ---"
    ps aux --sort=-%mem | head -6
    echo ""

} | tee "$LOG_FILE"

echo "Report saved to $LOG_FILE"