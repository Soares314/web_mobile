from django.forms import ModelForm
from turma.models import Turma

class TurmaForm(ModelForm):
    class Meta:
        model = Turma
        exclude = []