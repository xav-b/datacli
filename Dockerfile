FROM python:3.4
MAINTAINER Team Seeding

ADD requirements.txt /tmp/requirements.txt

RUN pip install \
  -r /tmp/requirements.txt \
  ipython

CMD ["ipython"]
