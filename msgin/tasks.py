from __future__ import absolute_import
from msgin.celery import app
from msgin.models import Message


@app.task
def scheduled_message(m_id):
    message = Message.objects.get(id=m_id)
    message.status = 'SEND'
    message.save()
