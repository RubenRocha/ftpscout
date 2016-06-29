#!/bin/bash

# Example usage:
# ./cidr_scout.sh 192.168.1.0/24

# Uses nmap to convert an IP range in CIDR format to pass to ftpscout
cidr_list () {
        nmap -sL $1 | grep "Nmap scan report" | awk '{print $NF}' | tr -d '()'
}

# Send the list into the server to add to the queue 
scoutsend () {
        RND=$RANDOM$RANDOM
        FILE="/tmp/$RND"
        echo "Generating list..."
        cidr_list $1 > $FILE
        ./server.py $FILE
        rm /tmp/$RND
}

# Example usage:
# scoutsend 192.168.1.0/24

scoutsend $1