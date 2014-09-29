from django.db import models
from django.contrib.auth.models import User, Group

class Message(models.Model):
	sender = models.ForeignKey(User, related_name = 'message_sender')
	user_recieiver = models.ManyToManyField(User, related_name = 'message_receiver', null = True, blank = True)
	group_receiver = models.ManyToManyField(Group, null = True, blank = True)
	message_content = models.TextField()
	send_time = models.DateTimeField('Scheduled Date & Time',null = True, blank = True)
	MESSAGE_STATUS = (('OUTBOX','Outbox'),('SEND','Send'),('SEEN','Received'))
	status=models.CharField(max_length = 6, choices = MESSAGE_STATUS)

'''class Receiver(models.Model):
	message=models.ForeignKey(Message)
	receiver=models.ForeignKey(User)'''

	
# Create your models here.
