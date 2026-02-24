#!/bin/bash

# Prompts the user for a filename and checks whether it exists.
# If it does, reports whether the file is readable, writable, and executable.

read -rp "Enter filename: " file


if [[ -f $file ]]; then
    echo "File exists"
    ls -l $file

    if [[ -r $file ]]; then
        echo "File is readable"
    else
        echo "File is not readable"
    fi

    if [[ -w $file ]]; then
        echo "File is writable"
    else
        echo "File is not writable"
    fi

    if [[ -x $file ]]; then
        echo "File is executable"
    else
        echo "File is not executable"
    fi

else
    echo "File does not exist"

fi