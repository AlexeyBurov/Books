# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0017_auto_20170928_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealer',
            name='materials',
        ),
        migrations.RemoveField(
            model_name='materialdealerprice',
            name='dealer',
        ),
        migrations.RemoveField(
            model_name='materialdealerprice',
            name='material',
        ),
        migrations.AddField(
            model_name='materialdealerprice',
            name='dealer_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='materialdealerprice',
            name='material_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]