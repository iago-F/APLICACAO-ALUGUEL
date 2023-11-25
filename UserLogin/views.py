from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required



#Função para cadastrar usuário. 
def cadastroUser(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        password = request.POST.get('senha')
        CPF = request.POST.get('CPF')

        user = User.objects.filter(username=username).first()

        if  user:
            return HttpResponse('usuario ja cadastrado')
        
        user = User.objects.create_user(username=username, email=email, password=password , first_name = first_name , last_name = last_name)
        user.save()
    
        
        return render(request, 'Login.html')



        

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
            return redirect('HomePage')  
        else:
            
            return render(request, 'Login.html', {'Login_iinvalido': True})

    return render(request, 'Login.html')


#funcção para acessar plataforma        
def plataforma(request):
   
     if request.user.is_authenticated:
         return render(request, 'plataforma.html')
     return HttpResponse('precisa estar logado')


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
        # user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        # Atualize outros campos conforme necessário

        user.save()
        return redirect('plataforma')
    

#função para fazer o Logout
@login_required(login_url="/auth/Login/")
def custom_logout(request):
        logout(request)
        return redirect('HomePage')