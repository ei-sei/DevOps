#!/bin/bash

# Creates a bash_demo directory, writes a timestamped message to demo.txt,
# and displays the file contents. Exits if the directory already exists.

DIRECTORY="bash_demo"
TIMESTAMP=$(date +%Y-%m-%d)

if [[ -d "$DIRECTORY" ]]; then
    echo "Error: Directory already exists"
    exit 1

else
    mkdir "$DIRECTORY"
    echo "$DIRECTORY created"
    cd "$DIRECTORY"

    touch demo.txt
    echo "demo.txt created"

    echo "This file was created by a Bash script on $TIMESTAMP" >> demo.txt
    cat demo.txt

fi



