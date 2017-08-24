#!/bin/bash
# Checks first if this was or not a pull request and calls the
# appropriate scripts

if [ "$TRAVIS_PULL_REQUEST" != "false" ];
then
  bash run_pull_requests.sh
  echo "Running on Pull Request \n \n ";

elif ["$TRAVIS_PULL_REQUEST" == "false"];
then
  bash run_merge.sh
  echo "Merged pull request found";

else
  echo "Unknown event ocurred";

fi;
