# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-29 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DutyLog', '0004_roletable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roletable',
            name='roleflag',
            field=models.CharField(max_length=128),
        ),
    ]