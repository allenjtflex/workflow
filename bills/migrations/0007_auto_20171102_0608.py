# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-01 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0006_bill_paied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='is_valid',
            field=models.BooleanField(default=False, verbose_name='單據作廢'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='paied',
            field=models.BooleanField(default=False, verbose_name='已付款'),
        ),
    ]
