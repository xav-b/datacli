#! /usr/bin/env bash

__DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"   )" && pwd   )"
DRILL_DL_URL="http://apache.mesi.com.ar/drill"
DEFAULT_PKG_PATH=/opt
DEFAULT_DRILL_VERSION="1.7.0"
DEFAULT_CONTAINER_IMAGE="hack/drill"

dl_tar() {
  local archive_url="${1}"
  local unpack_path="${2:-${DEFAULT_PKG_PATH}}"

  curl ${archive_url} | tar xvzf - -C ${unpack_path}
}

configure_storage() {
  local storage_cfg_file=${1:-/opt/drill-storage.json}
  local drill_server_url=${2:-"http://localhost:8047"}

  curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d @${storage_cfg_file} \
    ${drill_server_url}/storage/myplugin.json
}

start_container() {
  local container_image=${1:-"${DEFAULT_CONTAINER_IMAGE}"}
  docker run -d -it --name drill -p=8047:8047 ${container_image}
}

build_container() {
  local container_image=${1:-"${DEFAULT_CONTAINER_IMAGE}"}
  cd ${__DIR} && docker build --rm -t ${container_image} .
}

bootstrap() {
  local drill_version=${1:-"${DEFAULT_DRILL_VERSION}"}
  local pkg_url="${DRILL_DL_URL}/drill-${drill_version}/apache-drill-${drill_version}.tar.gz"

  echo "downloading ${pkg_url}"
  dl_tar ${pkg_url}
}

if [[ "$1" == "bootstrap" ]]; then
  #shift
  bootstrap $2
elif [[ "$1" == "storage" ]]; then
  configure_storage $2 $3
elif [[ "$1" == "build" ]]; then
  build_container $2
elif [[ "$1" == "run" ]]; then
  # TODO safe run (like already running)
  # TODO build it if necessary
  start_container $2
else
  echo "unknown command '$1'"
  exit 1
fi
