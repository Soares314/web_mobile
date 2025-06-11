from django.shortcuts import render, redirect
from django.views import View

class ListarTurmas(View):
    def get(self, request):
        return redirect('login')  
