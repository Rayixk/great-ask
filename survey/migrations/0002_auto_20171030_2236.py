# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-30 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='创建日期'),
        ),
    ]