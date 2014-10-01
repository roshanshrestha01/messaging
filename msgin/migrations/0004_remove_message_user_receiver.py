# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msgin', '0003_auto_20140930_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='user_receiver',
        ),
    ]
