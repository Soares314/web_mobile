from django.db import models
from users.models import Perfil

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    tutor = models.ManyToManyField(Perfil)