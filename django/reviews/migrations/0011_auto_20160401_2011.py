# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-01 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20160401_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='addr',
            field=models.CharField(max_length=100, verbose_name='Type your email address here please'),
        ),
    ]
