# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0003_auto_20150831_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='registered',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
