#!/bin/bash

echo "Gues the number between 0 to 10, inlusively"

read guess

random_numb=$(($RANDOM%11))

echo "Guessed: $guess, random:$random_numb"

if [ $guess -eq $random_numb ]
then
    echo "Correct Guess!"
else
    echo "Incorrect Guess!"
fi
