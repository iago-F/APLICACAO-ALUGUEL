from django.urls import path
from . import views


urlpatterns = [
    path('HomePage/',views.imagens_aleatorias, name='HomePage'),
    path('detalhes_casa/<int:casa_id>/', views.visualizar_detalhes_casa, name='detalhes_casa'),
]