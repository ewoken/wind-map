#!/bin/sh

# rm -rf tmp 

mkdir -p ./cache
mkdir -p ./outputs
mkdir -p ./tmp

python index.py

if [ -f "./tmp/BUILD_DONE.txt" ]; then
    echo "Build is done. Exit"
    exit 0
fi

if [ ! -f "./tmp/RESULT_MESSAGE.txt" ]; then
    echo "Build should create a tmp/RESULT_MESSAGE.txt. Error"
    exit 1
fi
