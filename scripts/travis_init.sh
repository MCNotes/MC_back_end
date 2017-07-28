
# Checks firs if this was or not a pull request and calls the
# approrpiate scripts
if [ "$TRAVIS_PULL_REQUEST" != "false" ]
then bash run_pull_requests.sh
echo "Running on Pull Request"

elif ["$TRAVIS_PULL_REQUEST" == "false"]
then bash run_merge.sh
echo "Merged pull request found"

fi
