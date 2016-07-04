FROM java:8

# install drill
ADD ./drill-storage.json /opt/drill-storage.json
ADD ./bootstrap.sh /opt/bootstrap-drill.sh
RUN /opt/bootstrap-drill.sh

# expose web server and api port
EXPOSE 8047 31010

# start a server and an repl
# TODO start drillbit and ipython
CMD ["/opt/apache-drill-1.7.0/bin/drill-embedded"]
