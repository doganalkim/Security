#!/bin/bash

fact(){
    parameter=$1
    if [[ parameter -lt 1 ]]
    then
        echo 1 # Return is used for raising errors
    else
        new_val=$(( parameter-1 ))
        recursive_result=$( fact $new_val ) 
        result=$(( recursive_result * parameter ))
        echo $result
    fi
}

res=$( fact $1 ) # This is the syntax for returning values
echo "Result is $res"
