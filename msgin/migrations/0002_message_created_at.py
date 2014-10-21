# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('msgin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2014, 10, 21), verbose_name=b'Created At'),
            preserve_default=False,
        ),
    ]
