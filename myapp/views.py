from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout, login
from myapp.forms import *
from django.contrib.auth.decorators import login_required
from myapp.models import Noticia, Evento, Ficheiro, Cidadao, Mensagem, Questionario
from django.db import models
from datetime import datetime
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django import http
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

import json
from django.http import JsonResponse


# Create your views here.

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

def index(request):
    news = show_news(request, 0)
    events = show_events(request)
    return render(request, 'index.html', {'user': request.user, 'news': news, 'events': events})


def questionario(request):
    return render(request, 'outros/questionario.html')


def mylogin(request):
    logout(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.getUser()
            login(request, user)
            return HttpResponseRedirect('/', {'user': request.user})
        else:
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@transaction.atomic
def register_page(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'], email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['nome'], last_name=form.cleaned_data['apelido'],
                                        is_active = '0')
            user.set_password(user.password)
            user.save()
            cidadao = Cidadao(user=user, num_bi=form.cleaned_data['num_bi'], morada=form.cleaned_data['morada'],
                                codigo_postal = form.cleaned_data['codigopostal'], localidade=form.cleaned_data['localidade'],
                                telefone = form.cleaned_data['telefone'], nro_eleitor = form.cleaned_data['nro_eleitor'])
            cidadao.save()
            token = default_token_generator.make_token(user)
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            uid = uid64.decode('utf-8')
            content = settings.SITE_URL+"/utilizador/ativar/"+uid+"/"+token;
            send_mail("Confirmar Registo na Junta de Freguesia", content, 'ricardoauxiliar@hotmail.com', [user.email], fail_silently=False)
            return render(request, 'registration/register.html', {'registered': True})
        else:
            #form = RegistrationForm()
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})


def activationview(request, uidb64, token):
    if uidb64 is not None and token is not None:
        from django.utils.http import urlsafe_base64_decode
        uid = force_text(urlsafe_base64_decode(uidb64))
        try:
            from django.contrib.auth import get_user_model
            from django.contrib.auth.tokens import default_token_generator
            user_model = get_user_model()
            user = user_model.objects.get(pk=uid)
            if default_token_generator.check_token(user, token) and user.is_active == 0:
                user_model.objects.filter(pk=uid).update(is_active='1')
                return HttpResponseRedirect('/login')
        except:
            pass
    return http.HttpResponseRedirect("/error")


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


def questionario(request):
    return render(request, 'outros/questionario.html', {'titulo': "Questionários", 'user': request.user, 'quest': Questionario.objects.filter(ativo=True),
                                                        'opcao': '1'})

def questionario2(request, num=0):
    return render(request, 'outros/questionario.html', {'user': request.user, 'quest': Questionario.objects.filter(id=num),
                                                        'opcao': '2'})


def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        subject = request.POST.get('subject')

        try:
            Mensagem.objects.create(
                remetente=name,
                email=email,
                telefone=mobile,
                assunto=subject,
                mensagem=message
            )
            messages.success(request, 'Mensagem enviada com sucesso')
            return HttpResponseRedirect('/')
        except Exception as e:
            messages.error(request, 'Mensagem não enviada')
            return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')

#functions

def show_events(request):

    #ev = Evento(titulo='Jogo do Benfica', descricao='Ir ao estádio da luz ver o Benfica', data_evento=datetime.now())
    #ev2 = Evento(titulo='Sport Lisboa', descricao='Ola ola', data_evento=datetime.now())
    #ev3 = Evento(titulo='Gato Jonas', descricao='Fazer asneiras', data_evento=datetime.now())
    #ev.save()
    #ev2.save()
    #ev3.save()

    events_list = list(Evento.objects.all().values())

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

    json_data = json.dumps(items_list, default=myconverter)

    return json_data

############################## ADMIN VIEWS ############################


def admin(request):
    if request.user.username == 'admin':
        aprovar = show_aprovar(request)
        return render(request, 'admin/admin.html', {'aprovar': aprovar})
    else:
        messages.error(request, 'Não dispõe de permissões')
        return HttpResponseRedirect('/')


def show_aprovar(request):
    events_list = Cidadao.objects.filter(aprovado=False)
    return events_list


def add_questionario(request):
    if request.user.username == 'admin':
        if request.method == 'POST':
            form = QuestionarioForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin')
        else:
            form = QuestionarioForm()
            return render(request, 'admin/add_questionario.html', {'form': form})
    else:
        messages.error(request, 'Não dispõe de permissões')
        return HttpResponseRedirect('/')



############ OUTROS ############

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()