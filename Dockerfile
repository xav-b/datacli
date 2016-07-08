FROM python:3.4
MAINTAINER Team Seeding

ADD requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y build-essential python-dev libmysqld-dev
RUN pip install -r /tmp/requirements.txt

CMD ["ipython"]
