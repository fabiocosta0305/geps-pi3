from django.contrib import admin
from .models import Instituicao, Docente, DisponibilidadeDocente, Demanda, Estado, Cidade, Bairro, Regioes, \
    DisponibilidadeRegiao, DisponibilidadeBairro

# Register your models here.
admin.site.register(Instituicao)
admin.site.register(Docente)
admin.site.register(DisponibilidadeDocente)
admin.site.register(Demanda)
admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Bairro)
admin.site.register(Regioes)
admin.site.register(DisponibilidadeRegiao)
admin.site.register(DisponibilidadeBairro)

