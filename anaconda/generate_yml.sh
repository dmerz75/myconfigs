#!/usr/bin/env bash

# Python 3.6.8 with pyspark 2.4.3 and fastparquet for local spark development
# gpl-3.0
# https://www.gnu.org/licenses/gpl-3.0.en.html

echo "my-environment: " $1 $2

export () {
    conda env export -n $1 -f $1.yml
}

upload () {
    anaconda upload $1.yml
}

$1 $2