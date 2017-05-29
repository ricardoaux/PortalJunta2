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
    remetente = models.CharField(max_length=100)
    assunto = models.CharField(max_length=100)
    email = models.EmailField(max_length=60)
    mensagem = models.CharField(max_length=1000)
    telefone = models.IntegerField()


class Ocorrencia (Conteudo_Utilizador):
    OPCOES = (
        ("A1", "Acessos para cidadãos de mobilidade reduzida"),
        ("A2", "Animais abandonados"),
        ("A3", "Arbustos ou árvores na via pública"),
        ("A4", "Conservação da ilumincação pública"),
        ("A5", "Conservação de ruas e pavimentos"),
        ("A6", "Conservação do parque escolar"),
        ("A7", "Estacionamento de veículos"),
        ("A8", "Limpeza de valetas, bermas e caminhos"),
        ("A9", "Limpeza e conservação de espaços públicos"),
        ("A10", "Manutenção de ciclovias"),
        ("A11", "Manutenção e limpeza de contentores e ecopontos"),
        ("A12", "Manutenção, rega e limpeza de jardins"),
        ("A13", "Nomes ou numeração de ruas"),
        ("A14", "Poluição sonora"),
        ("A15", "Publicidade, outdoors e cartazes"),
        ("A16", "Recolha de lixo"),
        ("A17", "Rupturas de águas ou desvio de tampas"),
        ("A18", "Sinalização de trânsito"),
        ("A19", "Outras ocorrências"),
    )

    utilizador = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    categoria = models.CharField(max_length=20, choices=OPCOES)
    local = models.CharField(max_length=200)
    informacao = models.CharField(max_length=1000)
    imagem = models.ImageField(upload_to='ocorr_images/', blank=True, null=True)
