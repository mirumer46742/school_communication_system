# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0002_auto_20170621_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
