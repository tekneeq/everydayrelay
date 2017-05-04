# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-29 19:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_address_relayed_addr_cnt'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelayAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relay_email', models.CharField(max_length=100, verbose_name='Type your email here...')),
                ('user_name', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('user_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Address')),
            ],
        ),
    ]
