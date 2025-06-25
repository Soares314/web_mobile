from django.db import models
from perfil.models import Perfil
from turma.consts import *

class Propriedade(models.Model):
    ranking = models.BooleanField(default=True)
    privado = models.BooleanField(default=False)

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    materia = models.SmallIntegerField(choices=OPCOES_MATERIA)
    descricao = models.TextField(blank=True, null=True)
    tutor = models.ManyToManyField(Perfil, related_name='tutor_turma', blank=True)
    propriedades = models.OneToOneField(Propriedade, on_delete=models.CASCADE, blank=True, null=True)
    alunos = models.ManyToManyField(Perfil, related_name='aluno_turma', blank=True)
    
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        abstract = True

class Aviso(Evento):
    pass

class Aula(Evento):
    video = models.FileField(upload_to='turma/fotos', blank=True, null=True)
    presenca = models.JSONField(default=dict, blank=True, null=True)
    

class Atividade(Evento):
    anexos = models.FileField(upload_to='turma/fotos', blank=True, null=True)
    pontos = models.IntegerField(default=0)