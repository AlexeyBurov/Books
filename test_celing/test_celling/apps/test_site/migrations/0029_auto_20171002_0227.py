# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-01 23:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0028_settings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Settings',
            new_name='Setting',
        ),
    ]
