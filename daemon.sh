#!/bin/bash

# --boot + PATH -> returns PID
if [ "$1" = "--boot" ]; then
    "$2" &
    echo $!
    exit 0
fi

# --kill + PID -> status code
if [ "$1" = "--kill" ]; then
    pid="$2"
    echo "Killing daemon with PID: $pid"
    exit 0
fi

exit 1
