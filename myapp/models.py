from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Cidadao(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_bi = models.PositiveIntegerField(null=True, blank=True)
    morada = models.CharField(max_length=100, null=True, blank=True)
    codigo_postal = models.CharField(max_length=8, null=True, blank=True)
    localidade = models.CharField(max_length=30, null=True, blank=True)
    telefone = models.PositiveIntegerField(null=True, blank=True)
    nro_eleitor = models.PositiveIntegerField(null=True, blank=True)
    aprovado = models.BooleanField(default=False)


class Conteudo_Site(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=3000)
    data_insercao = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        abstract = True


class Noticia(Conteudo_Site):
    imagem = models.ImageField(upload_to='news_images/', blank=True, null=True)


class Evento(Conteudo_Site):
    data_evento = models.DateTimeField()
    imagem = models.ImageField(upload_to='events_images/', blank=True, null=True)


class Ficheiro(Conteudo_Site):
    OPCOES = (
        ("ACAO", "Plano de Acao"),
        ("CONTAS", "Relatorio de Contas"),
        ("ACTAS", "Actas de Reuniao"),
        ("OUTRO", "Outros"),
    )

    tipo = models.CharField(max_length=20, choices=OPCOES,
                  default="OUTRO")
    ficheiro = models.FileField(upload_to='documents/')


class Questionario(Conteudo_Site):
    quest = models.CharField(max_length=400)
    ativo = models.BooleanField(default=True)


class Pergunta(Conteudo_Site):
    ativo = models.BooleanField(default=True)


class Opcao(models.Model):
    pergunta = models.ForeignKey(Pergunta)
    texto = models.CharField(max_length=100)


class Votacao(models.Model):
    utilizador = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, null=False)
    respondido = models.ForeignKey(Opcao, on_delete=models.CASCADE, null=False)


class Conteudo_Utilizador(models.Model):
    data_insercao = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        abstract = True


class Mensagem (Conteudo_Utilizador):
    remetente = models.CharField(max_length=50)
    assunto = models.CharField(max_length=60)
    email = models.EmailField(max_length=50)
    mensagem = models.CharField(max_length=500)
    telefone = models.IntegerField()

