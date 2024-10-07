from django.urls import path
from . import views


urlpatterns = [  
    path('CadastroCasa/',views.cadastrarCasa, name='cadastroCasa'),
    path('fazer_reserva/<int:casa_id>/', views.fazer_reserva, name='fazer_reserva'),
    path('casas_reservadas/', views.Casas_Reservadas, name='casas_reservadas'),
    path('casas_do_usuario/', views.casas_do_usuario, name='casas_do_usuario'),
    path('excluir_casa/<int:casa_id>/', views.excluir_casa, name='excluir_casa'),
    path('listar_casas/', views.listar_casas, name='listar_casas'),
    path('excluir_reserva_casa/<int:reserva_id>/', views.excluir_reserva_casa, name='excluir_reserva_casa'),
    path('atualizar_casa/<int:casa_id>/', views.atualizar_casa, name='atualizar_casa'),
    path('pagamento/<int:reserva_id>/', views.redirecionar_pagamento, name='redirecionar_pagamento'),
]
