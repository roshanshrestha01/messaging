# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msgin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='send_time',
            field=models.DateTimeField(null=True, verbose_name=b'Scheduled Date & Time', blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(max_length=6, choices=[(b'OUTBOX', b'Outbox'), (b'SEND', b'Send'), (b'SEEN', b'Received')]),
        ),
    ]
