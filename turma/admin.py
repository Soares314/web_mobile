from django.contrib import admin
from turma.models import *

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'materia', 'tutores_cadastrados')
    search_fields = ['nome']

    def tutores_cadastrados(self, obj):
        return obj.tutor.exists()
    tutores_cadastrados.boolean = True
    tutores_cadastrados.short_description = 'Tutores cadastrados?'

admin.site.register(Turma, TurmaAdmin)