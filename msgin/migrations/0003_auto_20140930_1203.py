# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msgin', '0002_auto_20140929_1417'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='user_recieiver',
            new_name='user_receiver',
        ),
    ]
