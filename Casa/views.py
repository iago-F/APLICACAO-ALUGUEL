from django.shortcuts import render
from .forms import CasaForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Casa, Reserva
from django.contrib import messages
        
@login_required
def cadastrarCasa(request):
    if request.method == 'POST':
        form = CasaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            

        
    else:
        form = CasaForm()

    return render(request, 'CadastrarCasa.html',{'form':form})


# função para fazer a reserva da casa 
@login_required
def fazer_reserva(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)

    # Verifica se a casa já tem uma reserva
    if Reserva.objects.filter(casa=casa).exists():
        messages.error(request, 'Esta casa já foi reservada.')
        return redirect('detalhes_casa', casa_id=casa.id)

    # Cria a reserva associando a casa e o usuário
    Reserva.objects.create(casa=casa, usuario=request.user)

    # Redireciona para a página de detalhes da casa com uma mensagem de sucesso
    messages.success(request, 'Reserva realizada com sucesso.')
    return redirect('detalhes_casa', casa_id=casa.id)


#Função para listta as casas que o usuário tem reservadas
@login_required
def Casas_Reservadas(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    # Obtém todas as reservas do usuário atual
    reservas_do_usuario = Reserva.objects.filter(usuario=request.user)

    # Pode ser necessário passar mais informações para o template, dependendo do que você deseja exibir
    context = {'casa': casa, 'usuario_cadastrou': casa.usuario}

    return render(request, 'Casas_Reservadas.html', {'reservas': reservas_do_usuario})




def casas_do_usuario(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        # Obtém todas as casas cadastradas pelo usuário logado
        casas_do_usuario = Casa.objects.filter(usuario=request.user)
        
        # Adiciona as casas ao contexto
        context = {'casas_do_usuario': casas_do_usuario}
        
        return render(request, 'CasasUsuario.html', context)
    else:
        # Se o usuário não estiver autenticado, redireciona para a página de login
        return redirect('Login') 



def excluir_casa(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)

    # Verifica se o usuário tem permissão para excluir a casa
    if request.user == casa.usuario:
        casa.delete()
        return redirect('casas_do_usuario')
    else:
        # Caso o usuário não tenha permissão, você pode exibir uma mensagem ou redirecionar para outra página
        return render(request, 'mensagem_sem_permissao.html')

    


