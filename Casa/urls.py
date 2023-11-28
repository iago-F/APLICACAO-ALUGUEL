from django.urls import path
from . import views


urlpatterns = [  
    path('CadastroCasa/',views.cadastrarCasa, name='cadastroCasa'),
    path('fazer_reserva/<int:casa_id>/', views.fazer_reserva, name='fazer_reserva'),
    path('casas_reservadas/', views.Casas_Reservadas, name='casas_reservadas'),
    path('casas_do_usuario/', views.casas_do_usuario, name='casas_do_usuario'),
    path('excluir_casa/<int:casa_id>/', views.excluir_casa, name='excluir_casa'),
]