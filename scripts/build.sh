#!/bin/sh

if [ ! -d "./build" ]; then
    echo "No build directory, first step"
    mkdir ./build
    touch ./build/FIRST_STEP
fi

node test.js

if [ -f "./build/BUILD_DONE.txt" ]; then
    echo "Build is done. Exit"
    exit 0
fi

if [ ! -f "./build/RESULT_MESSAGE.txt" ]; then
    echo "Build should create a build/RESULT_MESSAGE.txt. Error"
    exit 1
fi

RESULT_MESSAGE=$(cat ./build/RESULT_MESSAGE.txt)

if [ ! -z "$GITHUB_TOKEN" ]; then
    echo "Github actions"
    git config user.name github-actions
    git config user.email github-actions@github.com
fi

git add .

if [ -f './build/FIRST_STEP' ]; then
    rm -rf ./build/FIRST_STEP
    echo "First step"
    git commit -m "$RESULT_MESSAGE"
else
    echo "Not first step, amend"
    git commit --amend -m "$RESULT_MESSAGE"
fi

git push -f
