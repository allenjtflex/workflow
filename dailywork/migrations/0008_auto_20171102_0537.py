# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailywork', '0007_auto_20171031_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailylog',
            name='opreateDesc',
            field=models.CharField(max_length=20),
        ),
    ]
