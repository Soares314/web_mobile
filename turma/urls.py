from django.urls import path, include
from turma.views import *

urlpatterns = [
    path('', ListarTurmas.as_view(), name='listar_turmas'),
]
