# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 17:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170128_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='author',
        ),
        migrations.RemoveField(
            model_name='page',
            name='author',
        ),
        migrations.DeleteModel(
            name='BlogPost',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]
