from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from turma.models import Turma

class ListarTurmas(LoginRequiredMixin, ListView):
    model = Turma
    context_object_name = 'turmas'
    template_name = 'listar.html'
    
class CriarTurma(LoginRequiredMixin, CreateView):
    model = Turma
    fields = ['nome', 'materia', 'tutor', 'alunos', 'propriedades']
    template_name = 'criar_turma.html'
    
    def form_valid(self, form):
        form.instance.tutor = self.request.user.perfil
        return super().form_valid(form)
    
    def get_success_url(self):
        return redirect('listar_turmas')
    
