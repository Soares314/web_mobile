from django.db import models
from perfil.models import Perfil
from turma.consts import *

class Propriedade(models.Model):
    ranking = models.BooleanField(default=True)
    privado = models.BooleanField(default=False)

class Aviso(models.Model):
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

class Aula(models.Model):
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    
class Atividade(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    anexos = models.FileField(upload_to='turma/fotos/anexos_atividade', blank=True, null=True)
    pontos = models.IntegerField(default=0)
    data = models.DateTimeField()

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    materia = models.SmallIntegerField(choices=OPCOES_MATERIA)
    tutor = models.ManyToManyField(Perfil, related_name='tutor_turma', blank=True)
    propriedades = models.OneToOneField(Propriedade, on_delete=models.CASCADE, blank=True, null=True)
    alunos = models.ManyToManyField(Perfil, related_name='alunos_turma', blank=True)
    avisos = models.ForeignKey(Aviso, on_delete=models.CASCADE, blank=True, null=True)
    aulas = models.ForeignKey(Aula, on_delete=models.CASCADE, blank=True, null=True)
    atividades = models.ForeignKey(Atividade, on_delete=models.CASCADE, blank=True, null=True)