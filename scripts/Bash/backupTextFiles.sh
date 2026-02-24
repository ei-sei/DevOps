 #!/bin/bash

# Copies all .txt files from a user-specified directory into a timestamped
# backup directory and displays the total count of files backed up.

TIMESTAMP=$(date +%Y%m%d_%H%M%S) 

read -rp "Enter source directory: " source

BACKUP_DIR="./backup_$TIMESTAMP"

mkdir "$BACKUP_DIR"
echo "Backup directory created: backup_$TIMESTAMP"

count=0
for file in $source/*.txt; do
    cp "$file" "$BACKUP_DIR"
    (( count++ ))
done

echo "Backup complete! Files backed up: $count"