from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout
from myapp.forms import *
from django.contrib.auth.decorators import login_required
from myapp.models import Noticia, Evento
from django.db import models
from datetime import datetime
from django.core.serializers import serialize

import json
from django.http import JsonResponse


# Create your views here.

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

def index(request):
    news = show_news(request)
    events = show_events(request)
    return render(request, 'index.html', {'user': request.user, 'news': news, 'events': events})


def questionario(request):
    return render(request, 'questionario.html')


def login(request):
    return render(request, 'registration/login.html')


def main_page(request):
    return render(request, 'homepage.html', {'user': request.user})


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            return HttpResponseRedirect('/')
    form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def show_heraldica(request):
    return render(request, 'freguesia/heraldica.html',  {'user': request.user})


def show_historia(request):
    return render(request, 'freguesia/historia.html',  {'user': request.user})


def show_composicao(request):
    return render(request, 'orgaos/assembleia_composicao.html',  {'user': request.user})


def show_executivo(request):
    return render(request, 'orgaos/junta_executivo.html',  {'user': request.user})



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

def show_news(request):
    Noticia.objects.filter(titulo='Petr').delete()
    Noticia.objects.filter(titulo='Benfica ganhou').delete()
    Noticia.objects.filter(titulo='Jonas o Gato').delete()
    news = Noticia(titulo='Petr', descricao="porhjshjhjdsa jhsjdh adks k lkjs")
    news2 = Noticia(titulo='Benfica ganhou', descricao="glorioso slb sakljaklj ksjakld  dsjhsd s")
    news3 = Noticia(titulo='Jonas o Gato', descricao="o jonas e um gato muito cromo kdsajks asjhjsa jsk sahkj asdjg ajk sa a")
    news.save()
    news2.save()
    news3.save()

    items_list = list(Noticia.objects.all().values().order_by('-id'))

    json_data = json.dumps(items_list, default=myconverter)

    return json_data


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

