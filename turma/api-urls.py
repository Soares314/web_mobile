from django.urls import path, include
from turma.views import *

urlpatterns = [
    path('', ListarAPITurmas.as_view(), name='listar-turmas-api'),
    path('delete/<int:pk>/', DeleteAPITurmas.as_view(), name='deletar-turma-api'),
]
