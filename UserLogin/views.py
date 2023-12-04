from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from datetime import datetime

#Função para cadastrar usuário. 
def cadastroUser(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        dt_nasc_str = request.POST.get('dt_nasc')
        telefone = request.POST.get('telefone')
        instagram = request.POST.get('instagram')

        # Converte a string de data para um objeto datetime
        dt_nasc = datetime.strptime(dt_nasc_str, '%y-%m-%d').date() if dt_nasc_str else None

        # Verifica se o usuário já existe
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            messages.error(request, 'Usuário já existe. Escolha outro nome de usuário.')
            return render(request, 'cadastro.html')

        # Cria o usuário
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        # Cria o perfil do usuário
        perfilDoUsuario = UserProfile.objects.create(
            user=user,
            cpf=cpf,
            dt_nasc=dt_nasc,
            telefone=telefone,
            instagram=instagram,
        )

        user.save()
        perfilDoUsuario.save()
        messages.success(request, 'Cadastro realizado com sucesso. Faça login para continuar.')
        return redirect('Login')

    return render(request, 'cadastro.html')




# def cadastroUser(request):
#     if request.method == 'GET':
#         return render(request, 'cadastro.html')
#     else:
#         username = request.POST.get('username')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('senha')
#         cpf = request.POST.get('cpf')
#         dt_nasc = request.POST.get('dt_nasc')
#         telefone = request.POST.get('telefone')
#         instagram = request.POST.get('instagram')
        

#         user = User.objects.filter(username=username).first()

#         if  user:
#               return render(
#                   request, 'cadastro.html', 
#                   {'first_name': first_name, 
#                    'last_name': last_name, 
#                    'email': email, 
#                 #    'cpf':cpf, 
#                 #    'dt_nasc': dt_nasc, 
#                 #    'telefone': telefone, 
#                 #    'instagram': instagram, 
#                 #    'senha': senha,
#                    'usuario_existe': True})
        
        
#         user = User.objects.create_user(
#             username=username, 
#             email=email, 
#             password=password , 
#             first_name = first_name , 
#             last_name = last_name
#         )
#         user.save()

        
        
#         perfilDoUsuario = UserProfile.objects.create(
#                 user = user,
#                 cpf = cpf,
#                 dt_nasc = dt_nasc,
#                 telefone = telefone,
#                 instagram = instagram,  
#         )        
#         perfilDoUsuario.save()

        
#         return render(request, 'Login.html')



        

#Função para fazer Login
def Login(request):
    if request.method == "GET":
        return render(request, 'Login.html')
    elif request.method == "POST":
        username = request.POST.get('nome')
        senha = request.POST.get('senha')

        user = authenticate(request, username=username, password=senha)

        if user:
            login(request, user)
            return redirect('plataforma')  # Redirecione para a página desejada após o login bem-sucedido
        else:
            messages.error(request, 'Usuário ou senha incorreto')
            return render(request, 'Login.html')

    return render(request, 'Login.html')


# #funcção para acessar plataforma        
# def plataforma(request):
   
#      if request.user.is_authenticated:
#          return render(request, 'plataforma.html')
#      return HttpResponse('precisa estar logado')



def plataforma (request):
        #Obtém informações básicas do usuário autenticado
        if request.user.is_authenticated:
                user_info = {
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'email': request.user.email,
                        'username': request.user.username,
                }
        #Recupera informações adicionais em UserProfile do usuario 
        try:
                usuario = UserProfile.objects.get(user=request.user)
                perfil_info = {
                        'cpf': usuario.cpf,
                        'telefone': usuario.telefone,
                        'instagram': usuario.instagram,
                        'dt_nasc': usuario.dt_nasc,
                        }
        #Tratamento de exceção para inserir um dicionario vazio caso o UserProfile nao exista
        except UserProfile.DoesNotExist:
                perfil_info = {}  
        return render(request, 'plataforma.html', {'user_info': user_info, 'perfil_info': perfil_info})

# Função para excluir usuário autenticado
@login_required (login_url="/auth/DeletUsuario/")
def excluir_usuario_view(request):
     if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)  # Encerrar a sessão após excluir o usuário
        return redirect('Login')
        #  return render(request, 'template_excluir_conta.html')


#Função para atualizar os dados do usuário
def atualizar_perfil(request):
    if request.method == 'POST':
        user = request.user

        # Atualize os campos do usuário se estiverem presentes no formulário
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        # Atualize outros campos do usuário conforme necessário

        user.save()

        # Recupere o perfil do usuário associado
        perfilDoUsuario, created = UserProfile.objects.get_or_create(user=user)

        # Atualize os campos do UserProfile se estiverem presentes no formulário
        perfilDoUsuario.cpf = request.POST.get('cpf', perfilDoUsuario.cpf)
        perfilDoUsuario.dt_nasc = request.POST.get('dt_nasc', perfilDoUsuario.dt_nasc)
        perfilDoUsuario.telefone = request.POST.get('telefone', perfilDoUsuario.telefone)
        perfilDoUsuario.instagram = request.POST.get('instagram', perfilDoUsuario.instagram)
        # Atualize outros campos do UserProfile conforme necessário

        perfilDoUsuario.save()

        return redirect('plataforma')


#função para fazer o Logout
@login_required(login_url="/auth/Login/")
def custom_logout(request):
        logout(request)
        return redirect('HomePage')
