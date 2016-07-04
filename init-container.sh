#! /usr/bin/env bash

main() {
  docker exec -it $(basename $PWD)_mongo_1 /opt/bootstrap.sh

  # configure storage (todo)
  docker exec -it $(basename $PWD)_drill_1 /opt/bootstrap-drill.sh storage
}

main $@
