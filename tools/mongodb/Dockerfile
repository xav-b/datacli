FROM mongo:3.0.6

ADD ./bootstrap.sh /opt/

RUN curl -Lk -o /tmp/empinfo.json https://drill.apache.org/static/sql-on-mongodb/empinfo.json && \
  curl -Lk -o /tmp/zips.json http://media.mongodb.org/zips.json

EXPOSE 27017
