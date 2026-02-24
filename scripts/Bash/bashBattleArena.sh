#!/bin/bash

# Level 1: The Basics
# Mission: Create a directory named Arena and then inside it, create three files: warrior.txt, mage.txt, 
# and archer.txt. List the contents of the Arena directory.
mkdir Arena
cd Arena
touch warrior.txt mage.txt archer.txt
ls

# Level 2: Variables and Loops
# Mission: Create a script that outputs the numbers 1 to 10, one number per line.
for i in {1..10}; do
    echo "$i"
done


# Level 3: Conditional Statements
# Mission: Write a script that checks if a file named hero.txt exists in the Arena directory. 
# If it does, print Hero found!; otherwise, print Hero missing!.
if [[ -f "./arena/hero.txt" ]]; then
    echo "Hero found!"
else
    echo "Hero not found"
fi


# Level 4: File Manipulation
# Mission: Create a script that copies all .txt files from the Arena directory to a new directory called Backup.
if [[ -d "./backup" ]]; then
    echo "directory already exists"

else
    mkdir "./backup"
    for file in ./Arena/*.txt; do
        cp "$file" "./backup"
        echo "Copied $file"
    done
fi

# Level 5: Boss battle
# 1. Creates a directory names 'Battlefield'
# 2. Inside Battlefield, create files named knight.txt, sorcerer.txt, and rogue.txt.
# 3. Check if knight.txt exists; if it does, move it to a new directory called Archive.
# 4. List the contents of both Battlefield and Archive.
if [[ -d "./Battlefield" ]]; then
    echo "Battlefield already exists"

else
    mkdir "./Battlefield"
    touch ./Battlefield/knight.txt ./Battlefield/sorcerer.txt ./Battlefield/rogue.txt
fi


if [[ -f "./Battlefield/knight.txt" ]]; then
    if [[ -d "./Archive" ]]; then
        echo "Arhive already exists"

    else
        mkdir ./Archive
        mv ./Battlefield/knight.txt ./Archive
        echo "Sucessfully copied over to Archive"
    fi
else
    echo "Knight does not exist"
fi

ls ./Battlefield ./Archive


# Level 6: Argument Parsing
# Mission: Write a script that accepts a filename as an argument and prints the number of lines in that file. 
# If no filename is provided, display a message saying 'No file provided'.
filename="$1"

if [[ -z "$filename" ]]; then
    echo "No file provided"

else
    if [[ -f "$filename" ]]; then
        wc -l "$filename"

    else
        echo "file does not exist"
    fi
fi


# Level 7: File Sorting Script
# Mission: Write a script that sorts all .txt files in a directory by their size, from smallest to largest, 
# and displays the sorted list.
du -b *.txt | sort -n


# Level 8: Multi-File Searcher
# Mission: Create a script that searches for a specific word or phrase across all .log files in a directory 
# and outputs the names of the files that contain the word or phrase.
grep -l "error" *.log


# Level 9: Script to Monitor Directory Changes
# Mission: Write a script that monitors a directory for any changes (file creation, modification, or deletion) 
# and logs the changes with a timestamp.
DIRECTORY="Arena"
LOG_FILE="change_log.txt"

if [ ! -d "$DIRECTORY" ]; then
    echo "Directory does not exist."
    exit 1
fi

inotifywait -r "$DIRECTORY" | while read event; do
    if [ -e "$event" ]; then
        echo "$(date +'%Y-%m-%d %H:%M:%S') File modified/created: $event" >> "$LOG_FILE"
    else
        echo "$(date +'%Y-%m-%d %H:%M:%S') File deleted: $event" >> "$LOG_FILE"
    fi
done


# Level 10: Boss Battle 2 - Intermediate Scripting
# Mission: Write a script that:

# 1. Creates a directory called Arena_Boss.
# 2. Creates 5 text files inside the directory, named file1.txt to file5.txt.
# 3. Generates a random number of lines (between 10 and 20) in each file.
# 4. Sorts these files by their size and displays the list.
# 5. Checks if any of the files contain the word 'Victory', and if found, moves the file to a directory 
#    called Victory_Archive.

files=("file1.txt" "file2.txt" "file3.txt" "file4.txt" "file5.txt")

if [[ -d "Arena_Boss" ]]; then
    echo "Arena Boss already exists!"
    exit 0

else
    mkdir ./Arena_Boss
    for file in "${files[@]}"; do
        touch ./Arena_Boss/$file

        lines=$(( RANDOM % 11 + 10 ))
        seq 1 $lines >> ./Arena_Boss/$file
    done

    du -b ./Arena_Boss/*.txt | sort -n

fi

for file in "${files[@]}"; do
    if grep -q "Victory" ./Arena_Boss/$file; then
        mkdir -p ./Victory_Archive
        mv ./Arena_Boss/$file ./Victory_Archive
    else
        echo "no victory found"
    fi
done


# Level 11: Automated Disk Space Report
# Mission: Create a script that checks the disk space usage of a specified directory and sends an alert if 
# the usage exceeds a given threshold.
DIRECTORY="Arena"
THRESHOLD=1

USAGE=$(du -sm "$DIRECTORY" | awk '{print $1}')

if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "Warning: Disk usage for $DIRECTORY is at $USAGE%!"
else
    echo "Disk usage for $DIRECTORY is at $USAGE%. All is well."
fi


# Level 12: Simple Configuration File Parser
# Mission: Write a script that reads a configuration file in the format KEY=VALUE and prints each 
# key-value pair.
CONFIG_FILE="settings.conf"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Configuration file does not exists."
    exit 1
fi

while IFS='=' read -r key value; do
    echo "Key: $key, Value: $value"
done < "$CONFIG_FILE"

# Level 13: Backup Script with Rotation
# Mission: Create a script that backs up a directory to a specified location and keeps only the last 5 backups.
BACKUP="./Arena"
BACKUP_LOCATION="./Backup"

TIMESTAMP=$(date +%Y%m%d_%H%M%S) 

cp -r "$BACKUP" "$BACKUP_LOCATION/backup_$TIMESTAMP"

COUNT=$(ls -1 "$BACKUP_LOCATION" | wc -l)

if [[ $COUNT -gt 5 ]]; then
    ls -t "$BACKUP_LOCATION" | tail -n +6 | while read old; do
    rm -rf "$BACKUP_LOCATION/$old"
    done
fi


# Level 14: User-Friendly Menu Script
# Mission: Create an interactive script that presents a menu with options for different system tasks 
# (e.g., check disk space, show system uptime, list users), and executes the chosen task.
echo "Select an option:"
select task in "Check disk space" "Show system uptime" "List users" Quit; do
    case "$task" in
        "Check disk space")
            echo "You picked: $task"
            df -h
            ;;

        "Show system uptime")
            echo "You picked: $task"
            uptime
            ;;

        "List users")
            echo "You picked: $task"
            cut -d: -f1 /etc/passwd
            ;;

        Quit)
            echo "Bye!"
            break
            ;;
        *)
            echo "Invalid choice, try again"
            ;;
    esac
done


#!/bin/bash

# Level 15: Boss Battle 3 - Advanced Scripting
# Mission: Combine the skills you've gained! Write a script that:

# 1. Presents a menu to the user with the following options:
# - Check disk space
# - Show system uptime
# - Backup the Arena directory and keep the last 3 backups
# - Parse a configuration file settings.conf and display the values

echo "Choose an option:"
echo "1. Check disk space"
echo "2. Show system uptime"
echo "3. Backup the Arena directory and keep the last 3 backups"
echo "4. Parse a configuration file settings.conf and display the values"

read -rp "Enter your choice [1-4]: " choice

case $choice in
    1) df -h ;;

    2) uptime ;;

    3)  BACKUP="./Arena"
        BACKUP_LOCATION="./Backup"

        TIMESTAMP=$(date +%Y%m%d_%H%M%S) 

        cp -r "$BACKUP" "$BACKUP_LOCATION/backup_$TIMESTAMP"

        COUNT=$(ls -1 "$BACKUP_LOCATION" | wc -l)

        if [[ $COUNT -gt 3 ]]; then
            ls -t "$BACKUP_LOCATION" | tail -n +4 | while read old; do
            rm -rf "$BACKUP_LOCATION/$old"
            done
        fi ;;
        

    4) CONFIG_FILE="settings.conf"

        if [ ! -f "$CONFIG_FILE" ]; then
            echo "Configuration file does not exists."
            exit 1
        fi

        while IFS='=' read -r key value; do
            echo "Key: $key, Value: $value"
        done < "$CONFIG_FILE" ;;

    *) echo "Invalid option" ;;
esac