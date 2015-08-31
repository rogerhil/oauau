# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_auto_20150828_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='provider',
            field=models.CharField(max_length=32, default='mailchimp'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='list',
            unique_together=set([('provider', 'list_id', 'name')]),
        ),
    ]
