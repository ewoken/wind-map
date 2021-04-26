RESULT_MESSAGE=$(cat ./tmp/RESULT_MESSAGE.txt)

echo "Github actions"
git config user.name github-actions
git config user.email github-actions@github.com
git add .
git commit --amend -m "$RESULT_MESSAGE"
git push -f