from django.contrib import admin
from .models import Instituicao, Docente, DisponibilidadeDocente, Demanda


# Register your models here.
admin.site.register(Instituicao)
admin.site.register(Docente)
admin.site.register(DisponibilidadeDocente)
admin.site.register(Demanda)

