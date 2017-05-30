from django.contrib.auth import authenticate
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from myapp.models import Ficheiro, Cidadao, Questionario, Pergunta, Opcao, Noticia, Evento, Ocorrencia
from datetime import datetime, timezone


class LoginForm(forms.Form):
    user = None
    username = forms.CharField(label="Username", max_length=30,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                                   widget=forms.TextInput(
                                       attrs={'type': 'password', 'name': 'password', 'class': 'form-control'}))


    def clean(self):
        global user
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("O utilizador e a password não correspondem")
        if not user.is_active:
            raise forms.ValidationError("O utilizador não está activo")
        if not user.is_superuser:
            cidadao = Cidadao.objects.get(user=user)
            aproved = cidadao.aprovado
            if not aproved:
                raise forms.ValidationError('O utilizador ainda não foi aprovado')
        return self.cleaned_data

    def getUser(self):
        global user
        return user


class UserCreationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True)
    password1 = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)',
                        widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', required=True)
    nome = forms.CharField(label='Nome', max_length=30, required=True)
    apelido = forms.CharField(label='Apelido', max_length=30, required=True)
    num_bi = forms.IntegerField(label='Número do CC', required=True)
    morada = forms.CharField(label='Morada', max_length=100, required=True)
    codigopostal = forms.CharField(label='Código Postal', max_length=8, required=True)
    localidade = forms.CharField(label='Localidade', max_length=30, required=True)
    telefone = forms.IntegerField(label='Telefone', required=True)
    nro_eleitor = forms.IntegerField(label='Número de Eleitor', required=True)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('A Password não corresponde')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('O nome de utilizador apenas pode conter caracteres alfanuméricos')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('O nome de utilizador já existe')

    def clean_num_bi(self):
        if 'num_bi' in self.cleaned_data:
            num_bi = self.cleaned_data['num_bi']
            if len(str(num_bi)) != 8:
                raise forms.ValidationError('O número do CC é inválido (8 digitos)')
            else:
                try:
                    Cidadao.objects.get(num_bi = num_bi)
                except ObjectDoesNotExist:
                    return num_bi
                raise forms.ValidationError('O número do BI já existe')

    def clean_codigopostal(self):
        if 'codigopostal' in self.cleaned_data:
            codigopostal = self.cleaned_data['codigopostal']
            r = re.compile('.{4}-.{3}')
            if len(str(codigopostal)) != 8:
                raise forms.ValidationError('O código de postal é inválido (exemplo: 0000-000)')
            elif not r.match(codigopostal):
                raise forms.ValidationError('O código de postal é inválido (exemplo: 0000-000)')
            else:
                return codigopostal

    def clean_telefone(self):
        if 'telefone' in self.cleaned_data:
            telefone = self.cleaned_data['telefone']
            if len(str(telefone)) != 9:
                raise forms.ValidationError('O número de telefone é inválido (9 digitos)')
            else:
                return telefone

#
# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Ficheiro
#         fields = ('titulo', 'descricao', 'tipo', 'ficheiro')
#
#
# class QuestionarioForm(forms.ModelForm):
#     class Meta:
#         model = Questionario
#         fields = ('titulo', 'descricao', 'quest')


class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = '__all__'


class OpcaoForm(forms.ModelForm):
    class Meta:
        model = Opcao
        fields = ('texto',)


class OcorrenciasForm(forms.ModelForm):
    local = forms.CharField(label='Morada Completa', max_length=100, required=True)
    informacao = forms.CharField(label='Descrição', max_length=1000, required=True, widget=forms.Textarea)

    class Meta:
        model = Ocorrencia
        fields = '__all__'
        exclude = ['utilizador']

# class NoticiaForm(forms.ModelForm):
#     class Meta:
#         model = Noticia
#         fields = ('titulo', 'descricao', 'imagem')

