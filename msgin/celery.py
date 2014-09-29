from __future__ import absolute_import

from celery import Celery

app = Celery('msgin',
             broker='redis://localhost:6379/0',
             backend='redis://localhost',
             include=['msgin.tasks'])

if __name__ == '__main__':
    app.start()