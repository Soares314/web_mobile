from rest_framework import serializers
from .models import Turma

class SerializadorTurma(serializers.ModelSerializer):

    nome_materia = serializers.SerializerMethodField()

    class Meta: 
        model = Turma
        exclude = []

    def get_nome_materia(self, instancia):
        return instancia.get_materia_display()