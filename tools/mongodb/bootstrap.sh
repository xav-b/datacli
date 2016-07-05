#! /bin/sh

main() {
  mongoimport --host localhost --db test --collection zips < /tmp/zips.json
  mongoimport --host localhost --db employee --collection empinfo < /tmp/empinfo.json
}

main $@
