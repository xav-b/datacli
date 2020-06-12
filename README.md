# Data Cli

> Productive no-sql data sources exploration with SQL, Pandas and
> shortcuts

| service               | status        |
| --------------------- |:-------------:|
| travis | [![Build Status](https://travis-ci.org/hackliff/mgocli.svg?branch=master)](https://travis-ci.org/hackliff/mgocli) |
| quay.io/hackliff/drill | [![Docker Repository on Quay](https://quay.io/repository/hackliff/drill/status "Docker Repository on Quay")](https://quay.io/repository/hackliff/drill) |

## Getting started

`make container.build` will start and initialize [MongoDB](), [Drill]()
and `datacli` with everything installed.

It is still possible to register external data sources :

```Bash
$ cp ./tools/drill/mongo-storage-plugin.json custom-storage.json
$ $EDITOR custom-storage.json
$ ./tools/drill/manage.sh storage ./custom-storage.json http://$(docker-machine ip default):8047
{
  "result" : "success"
}
```

## Usage

### Mgocli

```Bash
$ ./datacli/__main__.py -H $(docker-machine ip default) appturbo
[2016-07-06 06:38:24,564] datacli :: INFO   - connected to Drillbit
[ datacli::192.168.99.100::appturbo  ] >>> SHOW DATABASES
[2016-07-06 06:38:48,391] datacli :: INFO   - sending query to drill
[show databases]
      SCHEMA_NAME
0  INFORMATION_SCHEMA
1          cp.default
2         dfs.default
3            dfs.root
4             dfs.tmp

```

### Drill Repl

```sql
$ # query data
$ docker exec -it $(basename $PWD)_drill_1 /opt/apache-drill-1.7.0/bin/drill-localhost
0: jdbc:drill:drillbit=localhost> SHOW DATABASES;
+---------------------+
|     SCHEMA_NAME     |
+---------------------+
| INFORMATION_SCHEMA  |
| cp.default          |
| dfs.default         |
| dfs.root            |
| dfs.tmp             |
| nosqltest.employee  |
| nosqltest.local     |
| nosqltest.test      |
| sys                 |
+---------------------+
9 rows selected (0.244 seconds)

0: jdbc:drill:drillbit=localhost> SELECT * FROM nosqltest.test.zips
LIMIT 3;
+--------+----------+-------------------------+--------+--------+
|  _id   |   city   |           loc           |  pop   | state  |
+--------+----------+-------------------------+--------+--------+
| 01001  | AGAWAM   | [-72.622739,42.070206]  | 15338  | MA     |
| 01002  | CUSHMAN  | [-72.51565,42.377017]   | 36963  | MA     |
| 01005  | BARRE    | [-72.108354,42.409698]  | 4546   | MA     |
+--------+----------+-------------------------+--------+--------+
3 rows selected (0.325 seconds)

0: jdbc:drill:drillbit=localhost> !quit
```

