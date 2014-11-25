from django.db import models
from django.contrib.auth.models import User, Group


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages')
    user_receiver = models.ManyToManyField(
        User,
        related_name='users',
        null=True,
        blank=True)
    group_receiver = models.ManyToManyField(Group, null=True, blank=True)
    message_content = models.TextField()
    send_time = models.DateTimeField(
        'Scheduled Date & Time',
        null=True,
        blank=True)
    MESSAGE_STATUS = (
        ('OUTBOX', 'Outbox'), ('SEND', 'Send'), ('SEEN', 'Received'))
    status = models.CharField(max_length=6, choices=MESSAGE_STATUS)
    created_at = models.DateTimeField('Created At')

    def __unicode__(self):
        return self.status
        # return ', '.join([f.user_receiver for f in self.user_receiver.all()])


# class Receiver(models.Model):
# 	message=models.ForeignKey(Message)
# 	receiver=models.ForeignKey(User)


# Create your models here.
