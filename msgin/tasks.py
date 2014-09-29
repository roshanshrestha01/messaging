from __future__ import absolute_import
from celery import Celery
from ms import settings
from msgin.celery import app
#from msgin.models import Message
#app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379/0')

@app.task
def scheduled_message(m_id):
	message=Message.objects.get(m_id)
	message.status='SEND'
	message.save()
    
