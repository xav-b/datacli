#! /usr/bin/env bash
# this file: initialize a working environment to test drill
#   - loads datasets into mongodb
#   - register mongodb as a drill data source

__DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

main() {
  docker exec -it $(basename $PWD)_mongo_1 /opt/bootstrap.sh

  # configure default storage (feel free to customize json file and rerun the
  # command, anytime)
  ${__DIR}/drill/manage.sh \
    storage \
    ${__DIR}/drill/mongo-storage-plugin.json \
    "http://$(docker-machine ip default):8047"
}

main $@
