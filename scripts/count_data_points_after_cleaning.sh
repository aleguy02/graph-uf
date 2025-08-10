#!/bin/bash

set -eo pipefail

tempf=$(mktemp)
JSON_PATH=$PWD/src/json

for f in $(ls $JSON_PATH/soc_cleaned*); do
        jq '.courses | length' $f >> $tempf
done

awk '{sum += $1} END {print sum}' $tempf
rm -f $tempf
