from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse('Você já está logado.')
        else:
            return render(request, 'auth_screen.html')
    
    def post(self, request):
        usuario = request.POST.get('nome', None)
        senha = request.POST.get('senha', None)
        
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                return render(request, 'auth_screen.html', {'error': 'Usuário está inativo'})
        else:
            return render(request, 'auth_screen.html', {'error': 'Usuário ou senha inválidos'})

class Logout(View):
    def post(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)
    
class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data= request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = self.get_token(user)
        return Response({
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'token': token.key
        })