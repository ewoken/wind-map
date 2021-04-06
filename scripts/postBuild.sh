#!/bin/sh

if [ -f "./build/BUILD_DONE.txt" ]; then
    echo "Build is done. Exit"
    exit 0
fi

if [ ! -f "./build/RESULT_MESSAGE.txt" ]; then
    echo "Build should create a build/RESULT_MESSAGE.txt. Error"
    exit 1
fi

RESULT_MESSAGE=$(cat ./build/RESULT_MESSAGE.txt)

git config user.name github-actions
git config user.email github-actions@github.com
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
