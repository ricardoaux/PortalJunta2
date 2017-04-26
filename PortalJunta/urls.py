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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from myapp.forms import LoginForm
from myapp import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin2/', views.admin, name="admin"),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'authentication_form': LoginForm},
        name='login'),
    url(r'^teste/$', views.main_page, name='homepage'),
    url(r'^logout/$', views.logout_page, name="logout_page"),
    url(r'^register/$', views.register_page, name="register_page"),
    url(r'^questionario/$', views.questionario, name="questionario"),
    url(r'^heraldica/$', views.show_heraldica, name="heraldica"),
    url(r'^historia/$', views.show_historia, name="historia"),
    url(r'^assembleia/composicao$', views.show_composicao, name="composicao"),
    url(r'^junta/executivo$', views.show_executivo, name="executivo"),
    url(r'^junta/competencias$', views.show_jcompetencias, name="junta_competencias"),
    url(r'^assembleia/competencias$', views.show_acompetencias, name="assembleia_competencias"),
    url(r'^noticias/all$', views.noticias, name = "noticias"),
]