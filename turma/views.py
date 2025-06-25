from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from rest_framework.generics import ListAPIView, DestroyAPIView
from django.contrib.auth.mixins import LoginRequiredMixin
from turma.models import *
from turma.forms import *
from turma.serializers import *
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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
    
class VerficarAlunoMixin:
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        
        turma_id = self.kwargs.get('pk')
        turma = get_object_or_404(Turma, pk=turma_id)
        
        self.is_aluno_or_tutor = self.get_is_auluno_or_tutor(turma)

        if not self.is_aluno_or_tutor:
            return HttpResponseForbidden("Você não é um aluno desta turma.")
        
        return super().dispatch(request, *args, **kwargs)

    def get_is_auluno_or_tutor(self, turma):
        user = self.request.user
        perfil = user.perfil
        return perfil in turma.alunos.all() or turma.tutor.filter(user=user).exists()

class ListarTurmas(LoginRequiredMixin, ListView):
    model = Turma
    context_object_name = 'turmas'
    template_name = 'listar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        perfil = user.perfil
        turmas = context['turmas']
        for turma in turmas:
            turma.esta_turma = perfil in turma.alunos.all()
            turma.e_o_tutor = turma.tutor.filter(user=user).exists()
        return context

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
    
class AcessarTurma(LoginRequiredMixin, VerficarAlunoMixin, DetailView):
    model = Turma
    context_object_name = 'turma'
    template_name = 'turma.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        turma = self.object
        avisos = Aviso.objects.filter(turma=turma)
        atividades = Atividade.objects.filter(turma=turma)
        aulas = Aula.objects.filter(turma=turma)
        # Junta todos os eventos e ordena por data (campo 'data')
        eventos = list(avisos) + list(atividades) + list(aulas)
        eventos.sort(key=lambda x: x.data, reverse=True)
        context['e_o_tutor'] = self.object.tutor.filter(user=user).exists()
        context['eventos'] = eventos
        context['avisos'] = avisos
        context['atividades'] = atividades
        context['aulas'] = aulas
        return context
    
class EntrarTurma(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        perfil = request.user.perfil
        turma = Turma.objects.get(pk=kwargs['pk'])
        turma.alunos.add(perfil)
        print(f'Alunos da turma após adicionar: {[a.id for a in turma.alunos.all()]}')
        return redirect('listar-turmas')
    
class ListarAPITurmas(ListAPIView):
    serializer_class = SerializadorTurma
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Turma.objects.all()
    
class DeleteAPITurmas(DestroyAPIView):
    serializer_class = SerializadorTurma
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Turma.objects.all()

