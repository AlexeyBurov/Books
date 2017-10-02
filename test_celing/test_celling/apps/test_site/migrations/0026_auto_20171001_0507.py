# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-01 02:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0025_auto_20171001_0227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='celling_id',
        ),
        migrations.AddField(
            model_name='order',
            name='celling',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='test_site.Celling'),
            preserve_default=False,
        ),
    ]