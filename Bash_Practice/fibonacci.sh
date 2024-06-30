#!/bin/bash


fib(){
    if [[ $1 -lt 2 ]] 
    then
        echo 1
    else
        local first=$(( $1 - 1 ))
        local second=$(( $1 - 2 ))
        local res1=$( fib $first )
        local res2=$( fib $second )
        local res=$(( res1 + res2 ))
        echo $res
    fi
}

ans=$( fib $1 )
echo "Result: $ans"

