#!/bin/sh

rm -rf tmp 

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

RESULT_MESSAGE=$(cat ./tmp/RESULT_MESSAGE.txt)

if [ ! -z "$CI" ]; then
    echo "Github actions"
    git config user.name github-actions
    git config user.email github-actions@github.com
    git add .
    git commit --amend -m "$RESULT_MESSAGE"
    git push -f
fi
