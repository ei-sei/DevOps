#!/bin/bash

# Prompts the user for two numbers and performs addition, subtraction,
# multiplication, and division. Handles division by zero.

read -rp "Enter your first number:" num1
read -rp "Enter your second number:" num2

add=$(( $num1 + $num2 ))
subtract=$(( $num1 - $num2 ))
multiply=$(( $num1 * $num2  ))


echo "$num1 + $num2 = $add"
echo "$num1 - $num2 = $subtract"
echo "$num1 * $num2  = $multiply"

if [[ $num2 == 0 ]]; then
    echo " Can not divide by 0"

else
    divide=$(( $num1 / $num2 ))
    echo "$num1 / $num2  = $divide"
fi
