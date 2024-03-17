#!/bin/bash

# --boot -> echo PID
if [ "$1" = "--boot" ]; then
    python caezar.py > /dev/null 2>&1 & 
    echo "pid:$! "
    exit 0
fi

# --kill + PID -> status code
if [ "$1" = "--kill" ]; then
    kill "$2"
    exit 0
fi

exit 1
