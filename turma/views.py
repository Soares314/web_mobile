from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from turma.models import Turma
from turma.forms import TurmaForm
from django.urls import reverse_lazy

class ListarTurmas(LoginRequiredMixin, ListView):
    model = Turma
    context_object_name = 'turmas'
    template_name = 'listar.html'
    
class CriarTurma(LoginRequiredMixin, CreateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'novo.html'
    success_url = reverse_lazy('listar-turmas')

    def form_valid(self, form):
        response = super().form_valid(form)
        from perfil.models import Perfil
        perfil, _ = Perfil.objects.get_or_create(user=self.request.user)
        self.object.tutor.add(perfil)
        return response

class EditarTurma(LoginRequiredMixin, UpdateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'editar.html'
    success_url = reverse_lazy('listar-turmas')
    
class DeletarTurma(LoginRequiredMixin, DeleteView):
    model = Turma
    template_name = 'deletar.html'
    success_url = reverse_lazy('listar-turmas')
    
class AcessarTurma(LoginRequiredMixin, DetailView):
    model = Turma
    context_object_name = 'turma'
    template_name = 'turma.html'

