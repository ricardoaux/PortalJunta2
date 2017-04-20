from django.db import models

# Create your models here.


class Pessoa(models.Model):
    permissao = models.CharField(max_length=1)
    username = models.CharField(max_length=20)

    class Meta:
        abstract = True


class Cidadao(Pessoa):
    nome = models.CharField(max_length=20)
    apelido = models.CharField(max_length=20)
    num_bi = models.PositiveIntegerField()
    morada = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=8)
    email = models.EmailField()
    telefone = models.PositiveIntegerField()
    nro_eleitor = models.PositiveIntegerField()


class Conteudo_Site(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=3000)
    data_insercao = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        abstract = True


class Noticia(Conteudo_Site):
    imagem = models.BinaryField()


class Evento(Conteudo_Site):
    data_evento = models.DateField()
    imagem = models.BinaryField()

