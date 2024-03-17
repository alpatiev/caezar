#!/bin/bash

# --boot -> returns PID
if [ "$1" = "--boot" ]; then
    python caesar.py > /dev/null 2>&1 & 
    echo "pid:$! "
fi

# --kill + PID -> status code
if [ "$1" = "--kill" ]; then
    kill "$2"
fi

exit 1
