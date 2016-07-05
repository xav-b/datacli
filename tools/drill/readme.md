# Drill Container

- [Drill in 10 minutes](https://drill.apache.org/docs/drill-in-10-minutes/)

## Pre-requisites

_Other versions may work but it was tested with the one below, on Mac
OSX El Capitan_

```Bash
$ docker version
Client:
Version:      1.8.1
API version:  1.20
Go version:   go1.4.2
Git commit:   d12ea79
Built:        Thu Aug 13 02:49:29 UTC 2015
OS/Arch:      darwin/amd64

Server:
Version:      1.11.2
API version:  1.23
Go version:   go1.5.4
Git commit:   b9f10c9
Built:        2016-06-01T21:20:08.558909126+00:00
OS/Arch:      linux/amd64

$ docker-machine version
docker-machine version 0.6.0, build e27fb87
$ # 4GB of memory is mandatory
$ docker-machine create -d virtualbox --virtualbox-memory 4096 default

$ docker build --rm -t local/drill .
$ docker run -it --rm local/drill /opt/apache-drill-1.7.0/bin/drill-embedde
```
