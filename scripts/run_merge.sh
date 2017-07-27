if [ "$CI" == "true" ]; then
        REPO=`git config remote.origin.url`;
        SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:};
