#!/bin/bash

Status="NULL"
logName=$(date +"%d%m%Y_%H%M")
ScreenProcess="AlmawebScrape"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
if ! screen -list | grep -q ${ScreenProcess};
    then
        Status="not running"
    else
        Status="running"
fi

echo "Status: $Status"

if [[ $1 == "stop" ]]
    then
        if [[ $Status == "running" ]]
            then
                screen -S ${ScreenProcess} -p 0 -X quit
                echo "Stopped Executing"
            else
                echo "No Instance running."
        fi
    elif [[ $1 == "start" ]]
        then
            if [[ $Status == "running" ]]
                then
                    echo "There is already an Instance running."
                else
                    screen -L -Logfile ${DIR}/logs/${logName} -S tadoAPI -d -m  /usr/bin/python3 ${DIR}/almawebScrape.py
                    echo "Created new Instance"
            fi
    else
        echo "Please type start or stop"
        exit 1
fi
