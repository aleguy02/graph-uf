#!/bin/bash

set -eo pipefail

FILE=$PWD/src/json/soc_cleaned.json


echo "=== checking $FILE for duplicate course names ==="

duplicates=$(jq -r '.courses[].name' $FILE | sort | uniq -d)
if [ -z "$duplicates" ]; then
        echo "=== no duplicates found. success ==="
        exit
else
        echo "=== duplicates found. failure ==="
        sleep 1
        echo "$duplicates"
        exit 1
fi