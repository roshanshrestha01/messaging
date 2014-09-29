ms
==

django messaging app

**Requirements**
Django 1.7
python 2.7

Broker- Redis Server
pip install celery[redis]

**Install**
_Run redis-server_
_Run celery worker by executing the following command _
  _celery -A msgin worker -l info-
_msgin is the name of application_
_run django server_

