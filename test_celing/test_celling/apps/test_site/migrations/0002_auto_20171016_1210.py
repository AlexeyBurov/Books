# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-16 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='color',
            new_name='color_model',
        ),
        migrations.AddField(
            model_name='order',
            name='file_name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='for_remove',
            field=models.BooleanField(default=None),
        ),
    ]
