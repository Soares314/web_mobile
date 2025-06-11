from django.db import models
from users.models import Perfil
from turma.consts import *

class Propriedade(models.Model):
    funcao = models.CharField(max_length=100)

class Aviso(models.Model):
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)

class Aula(models.Model):
    conteudo = models.TextField()
    data_aula = models.DateTimeField(auto_now_add=True)
    
class Atividade(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    anexos = models.FileField(upload_to='turma/fotos/anexos_atividade', blank=True, null=True)
    pontos = models.IntegerField(default=0)
    data_entrega = models.DateTimeField()

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    materia = models.SmallIntegerField(choices=OPCOES_MATERIA)
    tutor = models.ManyToManyField(Perfil, related_name='tutor_turma')
    propriedades = models.ManyToManyField(Propriedade)
    alunos = models.ManyToManyField(Perfil, related_name='alunos_turma')
    avisos = models.ManyToManyField(Aviso, blank=True)
    aulas = models.ForeignKey(Aula, on_delete=models.CASCADE, blank=True, null=True)
    atividades = models.ForeignKey(Atividade, on_delete=models.CASCADE, blank=True, null=True)