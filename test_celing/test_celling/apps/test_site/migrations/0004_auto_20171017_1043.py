# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-17 10:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_site', '0003_auto_20171017_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='color_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='test_site.MaterialColor'),
        ),
    ]
