#!/bin/bash
../bin/runspec --config=$1 -T base --action=build int
../bin/runspec --config=$1 -T base --reportable int 
../bin/runspec -c $1 -r ref -n 3 int
