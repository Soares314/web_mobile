from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from turma.models import *
from turma.forms import *
from django.urls import reverse_lazy

class VerficarTutorMixin:
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        
        turma_id = self.kwargs.get('pk')
        turma = get_object_or_404(Turma, pk=turma_id)
        
        self.tutoria = self.get_is_tutor(turma)

        if not self.tutoria:
            raise PermissionDenied("Você não tem permissão para acessar esta página.")
        
        return super().dispatch(request, *args, **kwargs)

    def get_is_tutor(self, turma):
        user = self.request.user
        return turma.tutor.filter(user=user).exists()

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
    

class CriarEvento(VerficarTutorMixin, LoginRequiredMixin, CreateView):
    model = Evento
    template_name = 'novo_evento.html'

    def get_form_class(self):
        tipo = self.kwargs.get('tipo')
        if tipo == 'aviso':
            return AvisoForm
        elif tipo == 'aula':
            return AulaForm
        elif tipo == 'atividade':
            return AtividadeForm
        else:
            raise ValueError("Tipo de evento inválido")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = self.kwargs.get('tipo')
        return context
    
    def form_valid(self, form):
        form.instance.turma = Turma.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('acessar-turma', kwargs={'pk': self.kwargs['pk']})

class EditarTurma(VerficarTutorMixin, LoginRequiredMixin, UpdateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'editar.html'
    success_url = reverse_lazy('listar-turmas')
    
class DeletarTurma(VerficarTutorMixin, LoginRequiredMixin, DeleteView):
    model = Turma
    template_name = 'deletar.html'
    success_url = reverse_lazy('listar-turmas')
    
class AcessarTurma(LoginRequiredMixin, DetailView):
    model = Turma
    context_object_name = 'turma'
    template_name = 'turma.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        turma = self.object
        avisos = Aviso.objects.filter(turma=turma)
        atividades = Atividade.objects.filter(turma=turma)
        aulas = Aula.objects.filter(turma=turma)
        # Junta todos os eventos e ordena por data (campo 'data')
        eventos = list(avisos) + list(atividades) + list(aulas)
        eventos.sort(key=lambda x: x.data, reverse=True)
        context['eventos'] = eventos
        context['avisos'] = avisos
        context['atividades'] = atividades
        context['aulas'] = aulas
        return context
    
class EntrarTurma(LoginRequiredMixin, CreateView):
    model = Turma
    form_class = ConfirmaçãoForm
    template_name = 'juntar.html'
    
    def form_valid(self, form):
        perfil = self.request.user.perfil
        turma = Turma.objects.get(pk=self.kwargs['pk'])
        turma.alunos.add(perfil)
        return redirect('acessar-turma', pk=turma.pk)
    
    def get_success_url(self):
        return reverse_lazy('acessar-turma', kwargs={'pk': self.kwargs['pk']})

