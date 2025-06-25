from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from perfil.models import Perfil
from turma.forms import TurmaForm
from turma.models import Turma, Propriedade, Aviso, Aula, Atividade

class TestesModelTurma(TestCase):
    def setUp(self):
        self.instancia = Turma(
            nome="Turma Teste",
            materia=1,
            descricao="Descrição da Turma Teste"
        )

class ListarTurmasViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.perfil = Perfil.objects.get(user=self.user)
        self.client.force_login(self.user)
        self.turma = Turma.objects.create(nome='Turma Teste', materia=1)
        self.turma.tutor.add(self.perfil)
        self.url = reverse_lazy('listar-turmas')
        self.turma.save()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Turma Teste')

class TestesViewsCriarTurmas(TestCase):
    def setUp(self):
        self.user = User.objects.create(username = "teste", password="12345678")
        self.client.force_login(self.user)
        self.url = reverse_lazy('criar-turma')
        

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.context.get('form'),TurmaForm)

    def test_post(self):
        data = {
            'nome': 'Turma Teste',
            'materia': 1,
            'descricao': 'Descrição da Turma Teste'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('listar-turmas'))

        self.assertEqual(Turma.objects.count(),1)
        self.assertEqual(Turma.objects.first().nome,"Turma Teste")

class TestesViewEditarTurmas(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username = "teste", password="12345678")
        self.client.force_login(self.user)
        self.instacia= Turma.objects.create(nome="Turma Teste", materia=1, descricao="Descrição da Turma Teste")
        self.url = reverse('editar-turma',kwargs={'pk':self.instacia.pk})

    def test_nao_tutor(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,403)
    
    def test_get_tutor(self):
        self.instacia.tutor.add(self.user.perfil)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.context.get('object'),Turma)
        self.assertIsInstance(response.context.get('form'),TurmaForm)
        self.assertEqual(response.context.get('object').pk,self.instacia.pk)
        self.assertEqual(response.context.get('object').materia,self.instacia.materia)
        self.assertEqual(response.context.get('object').descricao,self.instacia.descricao)


class TestesViewsDeletarTurmas(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "teste", password="12345678")
        self.client.force_login(self.user)
        self.instacia= Turma.objects.create(nome="Turma Teste", materia=1, descricao="Descrição da Turma Teste")
        self.url = reverse('deletar-turma',kwargs={'pk':self.instacia.pk})

    def test_nao_tutor(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,403)

    def test_get_tutor(self):
        self.instacia.tutor.add(self.user.perfil)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(response.context.get('object'),Turma)
        self.assertEqual(response.context.get('object').pk,self.instacia.pk)
    
    def test_post(self):
        self.instacia.tutor.add(self.user.perfil)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, reverse('listar-turmas'))
        self.assertEqual(Turma.objects.count(),0)
        
class EntrarTurmaViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='aluno', password='alunopass')
        self.perfil = Perfil.objects.get(user=self.user)
        self.client.force_login(self.user)
        self.turma = Turma.objects.create(nome='Turma Teste', materia=1)

    def test_post(self):
        url = reverse_lazy('entrar-turma', kwargs={'pk': self.turma.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.turma.refresh_from_db()
        self.assertIn(self.perfil, self.turma.alunos.all())
