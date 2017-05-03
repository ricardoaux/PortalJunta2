"""PortalJunta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from myapp.forms import LoginForm
from myapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin2/$', views.admin, name="admin"),
    url(r'^admin2/documents/add$', views.simple_upload, name="upload_file"),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.mylogin, name='login'),
    url(r'^logout/$', views.logout_page, name="logout_page"),
    url(r'^register/$', views.register_page, name="register_page"),
    url(r'^questionario/$', views.questionario, name="questionario"),
    url(r'^heraldica/$', views.show_heraldica, name="heraldica"),
    url(r'^historia/$', views.show_historia, name="historia"),
    url(r'^assembleia/composicao/$', views.show_composicao, name="composicao"),
    url(r'^junta/executivo/$', views.show_executivo, name="executivo"),
    url(r'^junta/competencias/$', views.show_jcompetencias, name="junta_competencias"),
    url(r'^assembleia/competencias/$', views.show_acompetencias, name="assembleia_competencias"),
    url(r'^contactos/$', views.show_contactos, name="contactos"),
    url(r'^noticias/$', views.noticias),
    url(r'^noticias/(?P<num>[0-9].*)/$', views.noticias),
    url(r'^planosdeacao/$', views.show_acao, name="acao"),
    url(r'^contas/$', views.show_contas, name="contas"),
    url(r'^actas/$', views.show_atas, name="actas"),
    url(r'^outros/$', views.show_outros, name="outros"),
    url(r'^utilizador/ativar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activationview, name='user-activation-link'),
    url(r'^mensagem/add$', views.send_message, name="mensagem"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
