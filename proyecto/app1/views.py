from django.shortcuts import render
from django.views.generic.base import View
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.
def login(request):
    return render(request, 'login.html')

def inicio(request):
    return render(request, 'inicio.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def carrito(request):
    return render(request, 'carrito.html')

def cuenta(request):
    return render(request, 'cuenta.html')

def registro(request):
    return render(request, 'registro_usuario.html')