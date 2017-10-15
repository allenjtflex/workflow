# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-15 03:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dailylog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.DateField(auto_now_add=True)),
                ('start_at', models.CharField(max_length=20)),
                ('end_with', models.CharField(max_length=20)),
                ('opreate_desc', models.CharField(blank=True, max_length=30, null=True)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10)),
                ('uniprice', models.DecimalField(decimal_places=0, max_digits=10)),
                ('payrequest', models.BooleanField(default=False)),
                ('bill_number', models.CharField(blank=True, max_length=20, null=True)),
                ('invalid', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Uom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriotion', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='dailylog',
            name='uom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailywork.Uom'),
        ),
    ]
