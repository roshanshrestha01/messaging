# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('msgin', '0004_remove_message_user_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='user_receiver',
            field=models.ManyToManyField(related_name=b'message_receiver', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
