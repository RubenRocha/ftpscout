#!/bin/bash
#
# FTPScout Launcher - Version 0.1 Alpha
#
# Created by RubenRocha & Someguy123
#

declare -a pids

THREADS=$1
LOGFILE=$2
PYTHONEXE="/usr/bin/env python3"
SCOUTSCRIPT=ftpscout.py

touch $LOGFILE

#
# Script usage help
#

if [[ "$#" -lt 2 ]]; then
    echo "usage: ./launch.sh [number of threads] [logfile.txt]";
    exit;
fi


echo "NOTE: If you would like more concise monitoring, use 'tail -f $LOGFILE'"
sleep 3

#
# Fire up the processes, log their PID into pids array
#

for i in $(seq 1 $THREADS); do
    $PYTHONEXE "$SCOUTSCRIPT" "$LOGFILE" &
    pids[$i]=$!
done

#
# Clean-up processes on C-C
#

trap ctrl_c INT

function ctrl_c() {
    echo "Shutting down... Killing FTPScout processes:"
    for i in "${pids[@]}"; do
        kill -9 $i;
	echo "Killed [PID] $i";
    done
}

#
# Finally, monitor the output of the processes
#

wait
