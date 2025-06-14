from django.urls import path, include
from turma.views import *

urlpatterns = [
    path('', ListarTurmas.as_view(), name='listar-turmas'),
    path('novo/', CriarTurma.as_view(), name='criar-turma'),
    path('editar/<int:pk>/', EditarTurma.as_view(), name='editar-turma'),
    path('deletar/<int:pk>/', DeletarTurma.as_view(), name='deletar-turma'),
    path('<int:pk>/', AcessarTurma.as_view(), name='acessar-turma'),
    path('<int:pk>/<str:tipo>/novo/', CriarEvento.as_view(), name='criar-evento'),
    path('<int:pk>/entrar/', EntrarTurma.as_view(), name='entrar-turma'),
]
