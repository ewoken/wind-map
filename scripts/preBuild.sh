#!/bin/sh

if [ ! -d "./build" ]; then
    echo "No build directory, first step"
    mkdir ./build
    touch ./build/FIRST_STEP
fi
