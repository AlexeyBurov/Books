# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-01 23:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0027_auto_20171001_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('property_name', models.CharField(max_length=256)),
                ('property_value', models.CharField(max_length=256)),
            ],
        ),
    ]