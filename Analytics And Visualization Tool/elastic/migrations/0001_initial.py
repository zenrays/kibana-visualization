# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MobileDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('brand', models.CharField(max_length=30)),
                ('camera', models.IntegerField()),
                ('ram', models.IntegerField()),
                ('memory', models.IntegerField()),
                ('battery', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
    ]
