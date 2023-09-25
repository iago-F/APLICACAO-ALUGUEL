from django.shortcuts import render
from django.http import HttpResponse


def usuario(request):
    return  render(request, 'usuario.html')

