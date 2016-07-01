#!/bin/bash

# Example usage:
# ./cidr_scout.sh 192.168.1.0/24 127.0.0.1/24

# Send the list into the server to add to the queue 
scoutsend () {
        RND=$RANDOM$RANDOM
        FILE="/tmp/$RND"
        echo "Generating list..."
        ./cidr_scout.py ${@} > $FILE
        ./server.py $FILE
        rm /tmp/$RND
}

# Example usage:
# scoutsend 192.168.1.0/24
# scoutsend 192.168.1.0/24 127.0.0.1/24

scoutsend ${@}