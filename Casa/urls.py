from django.urls import path
from . import views


urlpatterns = [
    path('CadastroCasa/',views.cadastrarCasa, name='cadastroCasa'),


]