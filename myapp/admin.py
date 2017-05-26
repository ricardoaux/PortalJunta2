from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Cidadao, Noticia, Evento, Ficheiro, Questionario, Pergunta, Opcao


class CidadaoInline(admin.StackedInline):
    model = Cidadao
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (CidadaoInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class NoticiaAdmin(admin.ModelAdmin):
    list_display = ("titulo", 'data_insercao')


class FicheiroAdmin(admin.ModelAdmin):
    list_display = ("titulo", 'data_insercao', 'tipo')


class EventoAdmin(admin.ModelAdmin):
    list_display = ("titulo", 'data_evento', 'data_insercao')


class QuestionarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_insercao')


class OpcaoAdmin(admin.TabularInline):
    model = Opcao
    extra = 2


class PerguntaAdmin(admin.ModelAdmin):
    inlines = (OpcaoAdmin, )
    list_display = ('titulo', 'data_insercao', 'ativo')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Ficheiro, FicheiroAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Questionario, QuestionarioAdmin)
admin.site.register(Pergunta, PerguntaAdmin)


