#!/bin/bash

MONITORDIR="/home/prasad/Development/DataMigratorDemo/Processing_Folder/Job_dump"

inotifywait -m -t 60 -r -P -e moved_to -e create --includei '*_destination_details.yaml'  "$MONITORDIR" |
    echo "An XML file ('$filename') was created in the directory."
