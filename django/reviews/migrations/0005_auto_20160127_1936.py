# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20160127_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='addr',
            field=models.CharField(max_length=100, verbose_name='Type your email here...'),
        ),
    ]
