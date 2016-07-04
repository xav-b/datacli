# MongoDB Cli

## SQL

- [SQL To Mongo Mapping](https://docs.mongodb.com/manual/reference/sql-comparison/)

```sql
$ # load mongodb db tests
$ docker exec -it $(basename $PWD)_mongo_1 /opt/bootstrap.sh

$ # configure storage (todo)
$ docker exec -it $(basename $PWD)_drill_1 /opt/bootstrap.sh storage

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
```

