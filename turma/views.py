from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
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

