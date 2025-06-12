from django.urls import path, include
from turma.views import *

urlpatterns = [
    path('', ListarTurmas.as_view(), name='listar-turmas'),
    path('novo/', CriarTurma.as_view(), name='criar-turma'),
]
