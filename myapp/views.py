from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout
from myapp.forms import *
from django.contrib.auth.decorators import login_required
from myapp.models import Noticia
from django.db import models
from datetime import datetime
from django.core.serializers import serialize

import json
from django.http import JsonResponse


# Create your views here.


def index(request):
    response = show_news(request);
    print(response)
    return render(request, 'index.html', {'user': request.user, 'news': response})


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


@login_required
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


    #return JsonResponse(json_data, safe=False)


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

