#! /usr/bin/env bash

DRILL_DL_URL="http://apache.mesi.com.ar/drill"
DEFAULT_PKG_PATH=/opt

dl_tar() {
  local archive_url="${1}"
  local unpack_path="${2:-${DEFAULT_PKG_PATH}}"

  curl ${archive_url} | tar xvzf - -C ${unpack_path}
}

configure_storage() {
  local storage_cfg_file=${1:-/opt/drill-storage.json}
  local drill_server_url="http://localhost:8047"

  curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d @${storage_cfg_file} \
    ${drill_server_url}/storage/myplugin.json
}

main() {
  local drill_version=${1:-"1.7.0"}
  local pkg_url="${DRILL_DL_URL}/drill-${drill_version}/apache-drill-${drill_version}.tar.gz"

  java --version
  dl_tar ${pkg_url}
}

main $@
