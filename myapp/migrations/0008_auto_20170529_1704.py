# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 17:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0007_auto_20170528_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ocorrencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_insercao', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.CharField(choices=[('A1', 'Acessos para cidadãos de mobilidade reduzida'), ('A2', 'Animais abandonados'), ('A3', 'Arbustos ou árvores na via pública'), ('A4', 'Conservação da ilumincação pública'), ('A5', 'Conservação de ruas e pavimentos'), ('A6', 'Conservação do parque escolar'), ('A7', 'Estacionamento de veículos'), ('A8', 'Limpeza de valetas, bermas e caminhos'), ('A9', 'Limpeza e conservação de espaços públicos'), ('A10', 'Manutenção de ciclovias'), ('A11', 'Manutenção e limpeza de contentores e ecopontos'), ('A12', 'Manutenção, rega e limpeza de jardins'), ('A13', 'Nomes ou numeração de ruas'), ('A14', 'Poluição sonora'), ('A15', 'Publicidade, outdoors e cartazes'), ('A16', 'Recolha de lixo'), ('A17', 'Rupturas de águas ou desvio de tampas'), ('A18', 'Sinalização de trânsito'), ('A19', 'Outras ocorrências')], max_length=20)),
                ('local', models.CharField(max_length=200)),
                ('informacao', models.CharField(max_length=1000)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='ocorrencias_images/')),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='mensagem',
            name='assunto',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mensagem',
            name='email',
            field=models.EmailField(max_length=60),
        ),
        migrations.AlterField(
            model_name='mensagem',
            name='mensagem',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='mensagem',
            name='remetente',
            field=models.CharField(max_length=100),
        ),
    ]
