#!/bin/bash

transport=('car' 'train' 'bike' 'bus')

echo "${transport[@]}"

unset transport[3]

echo "${transport[@]}"


