from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/',views.cadastroUser, name='cadastro'),
    path('Login/',views.Login, name='Login'),
    path('plataforma/',views.plataforma, name="plataforma"),
    path('DeletUsuario/',views.excluir_usuario_view, name="Delet_usuario"),
    path('UpdateUsuario/',views.atualizar_perfil, name="Update_Usuario")
]