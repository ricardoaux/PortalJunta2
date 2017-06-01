from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import logout, login
from myapp.forms import *
from django.contrib.auth.decorators import login_required
from myapp.models import Noticia, Evento, Ficheiro, Cidadao, Mensagem, Questionario, Pergunta, Opcao, Votacao, Ocorrencia, Servico
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
from django.db.models import Count

import json


# Create your views here.

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

def index(request):
    news = show_news(request, 0)
    events = show_events(request)
    return render(request, 'index.html', {'user': request.user, 'news': news, 'events': events})


def auth_error(request):
    return render(request, 'error/erro_autenticao.html', status=404)


def my_404_view(request):
    return render(request, 'error/404.html', status=404)


#def questionario(request):
#    return render(request, 'outros/questionario.html')


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


@login_required(login_url='auth_error')
def requerimentos(request):
    if request.method == 'POST':
        user = request.user
        form = RequerimentoForm(request.POST, request.FILES)
        if form.is_valid():

            try:
                Requerimento.objects.create(
                    utilizador = user,
                    servico = form.cleaned_data['servico'],
                    descricao = form.cleaned_data['descricao'],
                    documento = form.cleaned_data['documento'],
                    envio = form.cleaned_data['envio'],
                    pagamento = form.cleaned_data['pagamento'],
                    estado = "Em análise"
                )
                if (form.cleaned_data['pagamento'] == "Pagar na Junta"):
                    messages.success(request, 'Requerimento Efetuado! Verique o Seu Estado Brevemente')
                    return HttpResponseRedirect('./..')
            except Exception as e:
                messages.error(request, 'Erro ao Submeter Requerimento')
                return HttpResponseRedirect('./..')
    else:
        form = RequerimentoForm()
    user = request.user
    cidadao = Cidadao.objects.filter(user=user)
    return render(request, 'servicos/requerimento.html', {'user':user, 'cidadao': cidadao, 'form': form})


@login_required(login_url='auth_error')
def ocorrencias(request):
    if request.method == 'POST':
        user = request.user
        form = OcorrenciasForm(request.POST, request.FILES)
        if form.is_valid():
            try:

                Ocorrencia.objects.create(
                    utilizador = user,
                    local = form.cleaned_data['local'],
                    categoria = form.cleaned_data['categoria'],
                    informacao = form.cleaned_data['informacao'],
                    imagem = form.cleaned_data['imagem']
                )

                messages.success(request, 'Ocorrência relatada com sucesso')
                return HttpResponseRedirect('./..')
            except Exception as e:
                messages.error(request, 'Erro ao comunicar ocorrência')
                return HttpResponseRedirect('./..')
    else:
        form = OcorrenciasForm()
    return render(request, 'outros/ocorrencias.html', {'form': form})


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


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
    return render(request, 'conteudos/noticias.html', {'user': request.user, 'news': news, 'num':num})


def eventos(request, num=0):
    events = show_events(request, num);
    return render(request, 'conteudos/atividades.html', {'user': request.user, 'events': events, 'num':num})


@login_required(login_url='auth_error')
def questionario(request):
    return render(request, 'outros/questionario.html', {'titulo': "Questionários", 'user': request.user, 'quest': Questionario.objects.filter(ativo=True),
                                                        'opcao': '1'})

@login_required(login_url='auth_error')
def questionario2(request, num=0):
    return render(request, 'outros/questionario.html', {'user': request.user, 'quest': Questionario.objects.filter(id=num),
                                                        'opcao': '2'})


@login_required(login_url='auth_error')
def votar(request, pergunta_id=0):
    if request.method == 'POST':
        user = request.user.id
        choice = request.POST.get('choice')
        try:
            voto = Votacao(None, user, pergunta_id, choice)
            voto.save()
            messages.success(request, 'Voto submetido')
            return HttpResponseRedirect('./..')
        except Exception as e:
            messages.error(request, 'Erro ao votar')
            return HttpResponseRedirect('./..')


@login_required(login_url='auth_error')
def show_votacao(request):
    return render(request, 'outros/votacoes.html', {'poll_query': Pergunta.objects.all().order_by('data_insercao'),
                                                    'opt': '1'})


@login_required(login_url='auth_error')
def show_votacao2(request, num):
    pergunta = Pergunta.objects.filter(id=num).order_by('data_insercao')
    opcoes = Opcao.objects.filter(pergunta=pergunta)
    control = Votacao.objects.filter(utilizador=request.user.id, pergunta=num)
    if control.count()!=0:
        messages.error(request, 'Já efetuou o seu voto anteriormente')
        return HttpResponseRedirect('./..')
    else:
        return render(request, 'outros/votacoes.html', {'poll_query': pergunta, 'opcoes': opcoes, 'opt': '2', 'num':num})


@login_required(login_url='auth_error')
def show_votos(request, num):
    temp2=[]
    temp=[]
    pergunta = Pergunta.objects.filter(id=num).order_by('data_insercao')
    opcao = Opcao.objects.filter(pergunta=pergunta)
    votos = Votacao.objects.filter(pergunta=pergunta).values('respondido__texto').annotate(total=Count('respondido')).order_by('-total')
    count = Votacao.objects.filter(pergunta=pergunta).count()

    for vot in votos:
        temp2.append(vot['respondido__texto'])
        perc = vot['total']/count * 100;
        perc = "{0:.2f}".format(perc)
        temp.append({'opt':vot['respondido__texto'],'qtd':vot['total'],'perc':perc})

    for op in opcao:
        if not op.texto in temp2:
            temp.append({'opt':op.texto,'qtd':'0','perc':'0'})

    return render(request, 'outros/votos.html', {'poll_query':temp, 'num':num})


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


def view_polls(request):
    return render(request, 'admin/perguntas.html', {'poll_query': Pergunta.objects.all().order_by('data_insercao'),
                                                    'opt': '1'})

def view_polls2(request, num):
    pergunta = Pergunta.objects.filter(id=num).order_by('data_insercao')
    opcoes = Opcao.objects.filter(pergunta=pergunta)
    return render(request, 'admin/perguntas.html', {'poll_query': pergunta, 'opcoes': opcoes, 'opt': '2', 'num':num})

#functions


def show_events(request, num=0):
    if num == 0:
        events_list = list(Evento.objects.all().values())
    else:
        events_list = list(Evento.objects.filter(id=num).values())

    json_data = json.dumps(events_list, default=myconverter)

    return json_data


def show_news(request, num=0):
    if num == 0:
        items_list = list(Noticia.objects.all().values().order_by('-id'))
    else:
        items_list = list(Noticia.objects.filter(id=num).values())

    json_data = json.dumps(items_list, default=myconverter)

    return json_data



############################## ADMIN VIEWS ############################

@login_required(login_url='auth_error')
def admin(request):
    if request.user.username == 'admin':
        aprovar = show_aprovar(request)
        mens = show_mensagens(request)
        ocorr = show_ocorrencias(request)
        return render(request, 'admin/admin.html', {'aprovar': aprovar, 'mens' : mens, 'ocorr': ocorr})
    else:
        messages.error(request, 'Não dispõe de permissões')
        return HttpResponseRedirect('/')


@login_required(login_url='auth_error')
def mensagem_redirect(request, num=0):
    return HttpResponseRedirect('/admin/myapp/mensagem/'+num)


@login_required(login_url='auth_error')
def ocorrencia_redirect(request, num=0):
    return HttpResponseRedirect('/admin/myapp/ocorrencia/'+num)


@login_required(login_url='auth_error')
def show_aprovar(request):
    events_list = Cidadao.objects.filter(aprovado=False)
    return events_list


@login_required(login_url='auth_error')
def show_mensagens(request):
    mensagens_list = Mensagem.objects.all().values().order_by('-data_insercao')
    return mensagens_list


@login_required(login_url='auth_error')
def show_ocorrencias(request):
    ocorrencias_list = Ocorrencia.objects.all().values().order_by('-data_insercao')
    return ocorrencias_list

# def add_questionario(request):
#     if request.user.username == 'admin':
#         if request.method == 'POST':
#             form = QuestionarioForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('admin')
#         else:
#             form = QuestionarioForm()
#         return render(request, 'admin/add_questionario.html', {'form': form})
#     else:
#         messages.error(request, 'Não dispõe de permissões')
#         return HttpResponseRedirect('/')
#
#
# def add_noticia(request):
#     if request.user.username == 'admin':
#         if request.method == 'POST':
#             form = NoticiaForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return redirect('admin')
#         else:
#             form = NoticiaForm()
#         return render(request, 'admin/add_noticias.html', {'form': form})
#     else:
#         messages.error(request, 'Não dispõe de permissões')
#         return HttpResponseRedirect('/')
#
#
# def add_evento(request):
#     if request.user.username == 'admin':
#         if request.method == 'POST':
#             form = EventoForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return redirect('admin')
#             #else:
#              #   messages.error(request, 'Erro ao inserir evento')
#              #   return redirect('admin')
#         else:
#             form = EventoForm()
#         return render(request, 'admin/add_eventos.html', {'form': form})
#     else:
#         messages.error(request, 'Não dispõe de permissões')
#         return HttpResponseRedirect('/')
#
#
# def simple_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('admin')
#     else:
#         form = DocumentForm()
#     return render(request, 'admin/upload_file.html', {
#         'form': form
#     })


@login_required(login_url='auth_error')
def add_pergunta(request):
    if request.user.username == 'admin':
        if request.method == 'POST':
            form = PerguntaForm(request.POST)
            if form.is_valid():
                new = form.save()
                return redirect('/admin2/pergunta/'+str(new.id)+'/add')
        else:
            form = PerguntaForm()
        return render(request, 'admin/add_pergunta.html', {'form': form})
    else:
        messages.error(request, 'Não dispõe de permissões')
        return HttpResponseRedirect('/')


@login_required(login_url='auth_error')
def add_opcao(request, pergunta_id):
    if request.user.username == 'admin':
        pergunta = Pergunta.objects.get(id=pergunta_id)
        if request.method == 'POST':
            form = OpcaoForm(request.POST)
            if form.is_valid():
                # uses false commit to save the poll as the current poll ID, sets the initial vote to 0, and saves all choices the user
                # has put in the form
                add_pergunta = form.save(commit=False)
                add_pergunta.pergunta = pergunta
                add_pergunta.save()
                form.save()
            return redirect('/admin2/pergunta/' + str(pergunta.id) + '/add')
        else:
            form = OpcaoForm()
        return render(request, 'admin/add_opcao.html', {'form': form, 'poll_id': pergunta_id})
    else:
        messages.error(request, 'Não dispõe de permissões')
        return HttpResponseRedirect('/')




############ OUTROS ############

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()
