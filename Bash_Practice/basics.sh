#!/bin/bash

name="Alkım" # Do not have spaces between variables
echo "Hello World"
echo $name

set -x #lines between -x and +x are debugged

whoami

id

set +x #end of debugging

age=21
echo "$name is $age yrs old"

