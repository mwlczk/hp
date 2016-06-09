# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-09 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160609_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug_de',
            field=models.CharField(help_text='Slug (used in URLs)', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug_en',
            field=models.CharField(help_text='Slug (used in URLs)', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='title_de',
            field=models.CharField(help_text='Page title', max_length=64),
        ),
        migrations.AlterField(
            model_name='page',
            name='title_en',
            field=models.CharField(help_text='Page title', max_length=64),
        ),
    ]
