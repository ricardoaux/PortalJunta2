from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.template import loader
from django.template import Context
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from myapp.forms import *
# Create your views here.


def index(request):
    return render(request, 'index.html', {'user': request.user})


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
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
            return HttpResponseRedirect('/')
    form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})