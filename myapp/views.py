from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout
from myapp.forms import *
from django.contrib.auth.decorators import login_required
from myapp.models import Noticia, Evento, Ficheiro, Cidadao
from django.db import models
from datetime import datetime
from django.core.serializers import serialize
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.db import transaction

import json
from django.http import JsonResponse


# Create your views here.

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

def index(request):
    news = show_news(request, 0)
    events = show_events(request)
    return render(request, 'index.html', {'user': request.user, 'news': news, 'events': events})


def admin(request):
    return render(request, 'admin/admin.html')


def questionario(request):
    return render(request, 'questionario.html')


def login(request):
    return render(request, 'registration/login.html')


def main_page(request):
    return render(request, 'homepage.html', {'user': request.user})


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@transaction.atomic
def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'], email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['nome'], last_name=form.cleaned_data['apelido'])
            user.save()
            cidadao = Cidadao(user=user, num_bi=form.cleaned_data['num_bi'], morada=form.cleaned_data['morada'],
                                codigo_postal = form.cleaned_data['codigopostal'], localidade=form.cleaned_data['localidade'],
                                telefone = form.cleaned_data['telefone'], nro_eleitor = form.cleaned_data['nro_eleitor'])
            cidadao.save()
            return render(request, 'registration/register.html', {'registered': True})
        else:
            print(form.errors)
            #form = RegistrationForm()
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})


def simple_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = DocumentForm()
    return render(request, 'admin/upload_file.html', {
        'form': form
    })


def show_acao(request):
  return render(request, 'outros/verpdf.html', {'user': request.user, 'titulo': "Planos de Ação", 'obj': Ficheiro.objects.filter(tipo="ACAO")})


def show_atas(request):
  return render(request, 'outros/verpdf.html', {'user': request.user, 'titulo': "Actas de Reuniões", 'obj': Ficheiro.objects.filter(tipo="ACTAS")})


def show_contas(request):
  return render(request, 'outros/verpdf.html', {'user': request.user, 'titulo': "Relatórios de Contas", 'obj': Ficheiro.objects.filter(tipo="CONTAS")})


def show_outros(request):
  return render(request, 'outros/verpdf.html', {'user': request.user, 'titulo': "Outros Documentos", 'obj': Ficheiro.objects.filter(tipo="OUTROS")})


def show_heraldica(request):
    return render(request, 'freguesia/heraldica.html',  {'user': request.user})


def show_historia(request):
    return render(request, 'freguesia/historia.html',  {'user': request.user})


def show_composicao(request):
    return render(request, 'orgaos/assembleia_composicao.html',  {'user': request.user})


def show_executivo(request):
    return render(request, 'orgaos/junta_executivo.html',  {'user': request.user})


def show_jcompetencias(request):
    return render(request, 'orgaos/junta_competencias.html',  {'user': request.user})


def show_acompetencias(request):
    return render(request, 'orgaos/assembleia_competencias.html',  {'user': request.user})


def show_contactos(request):
    return render(request, 'outros/contactos.html',  {'user': request.user})


def noticias(request, num=0):
    news = show_news(request, num);
    return render(request, 'conteudos/noticias.html', {'user': request.user, 'news': news})


#functions

def show_events(request):
    Evento.objects.all().delete()
    ev = Evento(titulo='Jogo do Benfica', descricao='Ir ao estádio da luz ver o Benfica', data_evento=datetime.now())
    ev2 = Evento(titulo='Sport Lisboa', descricao='Ola ola', data_evento=datetime.now())
    ev3 = Evento(titulo='Gato Jonas', descricao='Fazer asneiras', data_evento=datetime.now())
    ev.save()
    ev2.save()
    ev3.save()

    events_list = list(Evento.objects.all().values())
    print(events_list)

    json_data = json.dumps(events_list, default=myconverter)

    return json_data


def show_news(request, num=''):

    #Noticia.objects.filter(titulo='Petr').delete()
    #Noticia.objects.filter(titulo='Benfica ganhou').delete()
    #Noticia.objects.filter(titulo='Jonas o Gato').delete()
    #news = Noticia(titulo='Petr', descricao="porhjshjhjdsa jhsjdh adks k lkjs")
    #news2 = Noticia(titulo='Benfica ganhou', descricao="glorioso slb sakljaklj ksjakld  dsjhsd s")
    #news3 = Noticia(titulo='Jonas o Gato', descricao="o jonas e um gato muito cromo kdsajks asjhjsa jsk sahkj asdjg ajk sa a")
    #news.save()
    #news2.save()
    #news3.save()
    if num == 0:
        items_list = list(Noticia.objects.all().values().order_by('-id'))
    else:
        items_list = list(Noticia.objects.filter(id=num).values())

    print(items_list)
    json_data = json.dumps(items_list, default=myconverter)

    return json_data


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

