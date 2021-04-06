#!/bin/sh

if [ -f "./BUILD_DONE.txt" ]; then
    echo "Build is done. Exit"
    exit 0
fi

if [ ! -f "./RESULT_MESSAGE.txt" ]; then
    echo "Build should create a RESULT_MESSAGE.txt. Error"
    exit 1
fi

RESULT_MESSAGE=$(cat ./RESULT_MESSAGE.txt)

git config user.name github-actions
git config user.email github-actions@github.com
git add .
git commit --amend -m "$RESULT_MESSAGE"
git push -f
