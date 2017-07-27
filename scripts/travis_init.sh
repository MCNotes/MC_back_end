if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then bash run_pull_requests.sh

elif ["$TRAVIS_PULL_REQUEST" == "false"]; then bash run_merge.sh
