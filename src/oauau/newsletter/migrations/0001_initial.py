# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('list_id', models.CharField(unique=True, max_length=128)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, unique=True, max_length=100, blank=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('first_name', models.CharField(max_length=255, blank=True, null=True)),
                ('last_name', models.CharField(max_length=255, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('list', models.ForeignKey(to='newsletter.List')),
                ('subscriber', models.ForeignKey(to='newsletter.Subscriber')),
            ],
        ),
    ]
