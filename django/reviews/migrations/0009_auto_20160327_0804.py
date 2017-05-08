# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-27 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20160130_0514'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.AlterField(
            model_name='address',
            name='addr',
            field=models.CharField(max_length=100, verbose_name='Type email address to relay here...'),
        ),
    ]