# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-12 19:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20170412_1850'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Noticia',
        ),
        migrations.DeleteModel(
            name='Pessoa',
        ),
    ]