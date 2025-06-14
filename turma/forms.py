from django.forms import ModelForm
from turma.models import *

class ConfirmaçãoForm(ModelForm):
    class Meta:
        model = Propriedade
        exclude = []

class TurmaForm(ModelForm):
    class Meta:
        model = Turma
        exclude = []
        
class AvisoForm(ModelForm):
    class Meta:
        model = Aviso
        fields = ['titulo', 'descricao']
        
class AulaForm(ModelForm):
    class Meta:
        model = Aula
        fields = ['titulo', 'descricao', 'video']
        
class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade
        fields = ['titulo', 'descricao', 'pontos']