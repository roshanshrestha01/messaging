# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('msgin', '0005_message_user_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date',
            field=models.DateField(default=datetime.date(2014, 10, 7), verbose_name=b'Date'),
            preserve_default=False,
        ),
    ]
