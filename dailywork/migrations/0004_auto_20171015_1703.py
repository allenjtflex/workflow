# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-15 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dailywork', '0003_auto_20171015_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailylog',
            name='opreate_desc',
        ),
        migrations.AddField(
            model_name='dailylog',
            name='opreateDesc',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
    ]
