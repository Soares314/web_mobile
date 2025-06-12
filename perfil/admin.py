from django.contrib import admin
from perfil.models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ['user']
    
admin.site.register(Perfil, PerfilAdmin)