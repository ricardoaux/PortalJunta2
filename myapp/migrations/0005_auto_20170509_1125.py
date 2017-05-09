# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-09 11:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0004_auto_20170503_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=3000)),
                ('data_insercao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='pergunta',
            name='respostas',
            field=models.ManyToManyField(blank=True, to='myapp.Resposta'),
        ),
        migrations.AddField(
            model_name='pergunta',
            name='utilizadores',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
