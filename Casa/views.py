from django.shortcuts import render
from .forms import CasaForm , ReservaForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Casa, Reserva
from django.contrib import messages
from .forms import CasaForm , FiltroCasaForm
import datetime
from datetime import datetime
from django.db import transaction




@login_required
def cadastrarCasa(request):
    if request.method == 'POST':
        form = CasaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            

        
    else:
        form = CasaForm()

    return render(request, 'CadastrarCasa.html',{'form':form})






@login_required
def fazer_reserva(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)

    if request.method == 'POST':
        data_final_str = request.POST.get('data_final')

        if not data_final_str:
            messages.error(request, 'Por favor, escolha uma data para fazer a reserva.')
            return redirect('detalhes_casa', casa_id=casa.id)

        data_final = datetime.strptime(data_final_str, '%Y-%m-%d').date()

        # Verifica se a casa já tem uma reserva
        if Reserva.objects.filter(casa=casa, data_final__gte=data_final).exists():
            messages.error(request, 'Esta casa já foi reservada para a data escolhida.')
            return redirect('detalhes_casa', casa_id=casa.id)

        # Cria a reserva associando a casa, o usuário e a data final
        Reserva.objects.create(casa=casa, usuario=request.user, data_final=data_final)

        # Redireciona para a página de detalhes da casa com uma mensagem de sucesso
        messages.success(request, 'Reserva realizada com sucesso.')
        return redirect('detalhes_casa', casa_id=casa.id)

    return render(request, 'DetalhesCasa.html', {'casa': casa})
# def fazer_reserva(request, casa_id):
#     casa = get_object_or_404(Casa, id=casa_id)
#
#     if request.method == 'POST':
#         numero_cartao = request.POST.get('numero_cartao')
#         data_final_str = request.POST.get('data_final')
#
#         if not data_final_str:
#             messages.error(request, 'Por favor, escolha uma data para fazer a reserva.')
#             return redirect('detalhes_casa', casa_id=casa.id)
#
#         data_final = datetime.strptime(data_final_str, '%Y-%m-%d').date()
#
#         # Verifica se a casa já tem uma reserva
#         if Reserva.objects.filter(casa=casa, data_final__gte=data_final).exists():
#             messages.error(request, 'Esta casa já foi reservada para a data escolhida.')
#             return redirect('detalhes_casa', casa_id=casa.id)
#
#         # Cria a reserva associando a casa, o usuário e a data final
#         with transaction.atomic():
#             reserva = Reserva.objects.create(casa=casa, usuario=request.user, data_final=data_final)
#
#             # Obtém o valor da casa para usar no pagamento
#             valor_do_pagamento = casa.valor
#
#             # Cria a instância do Pagamento associada à reserva
#             pagamento = Pagamento.objects.create(casa=casa, usuario=request.user, numero_cartao=numero_cartao, valor=valor_do_pagamento, reserva=reserva)
#
#         # Redireciona para a página de detalhes da casa com uma mensagem de sucesso
#         messages.success(request, 'Reserva realizada com sucesso.')
#         return redirect('detalhes_casa', casa_id=casa.id)
#
#     return render(request, 'DetalhesCasa.html', {'casa': casa})
#




# FUNÇÃO PARA VER AS CASAS RESERVADAS
@login_required
def Casas_Reservadas(request):
    # Obtém todas as reservas do usuário atual
    reservas_do_usuario = Reserva.objects.filter(usuario=request.user)

    
    context = {'reservas': reservas_do_usuario}

    return render(request, 'Casas_Reservadas.html', context)


#Listar as casas do usuário
@login_required
def casas_do_usuario(request):
    # Obtém todas as casas cadastradas pelo usuário logado
    casas_do_usuario = Casa.objects.filter(usuario=request.user)

    # Adiciona as casas ao contexto
    context = {'casas_do_usuario': casas_do_usuario}

    return render(request, 'casas_do_usuario.html', context)


#Excluir casas
def excluir_casa(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)

    # Verifica se o usuário tem permissão para excluir a casa
    if request.user == casa.usuario:
        casa.delete()
        return redirect('casas_do_usuario')
    else:
        # Caso o usuário não tenha permissão, você pode exibir uma mensagem ou redirecionar para outra página
        return render(request, 'mensagem_sem_permissao.html')


#Excluir_Reserva 
def excluir_reserva_casa(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    # Verifica se o usuário tem permissão para excluir a casa
    if request.user == reserva.usuario:
        reserva.delete()
        return redirect('casas_reservadas')
    else:
        # Caso o usuário não tenha permissão, você pode exibir uma mensagem ou redirecionar para outra página
        return render(request, 'HomePage.html')
    

#Funcção para Filtrar as casas
def listar_casas(request):
    form = FiltroCasaForm(request.GET)

    if form.is_valid():
        escolha_critero = form.cleaned_data.get('escolha_critero')
        quantidade = form.cleaned_data.get('quantidade')

        # Filtra as casas com base nos critérios selecionados
        if escolha_critero == 'num_quartos':
            casas = Casa.objects.filter(num_quarto=quantidade)
        elif escolha_critero == 'num_banheiros':
            casas = Casa.objects.filter(num_banheiro=quantidade)
        elif escolha_critero == 'preco_total':
            casas = Casa.objects.filter(preco_total=quantidade)
        else:
            casas = Casa.objects.all()

        context = {'casas': casas, 'form': form}
        return render(request, 'listagem_casas.html', context)

    # Se o formulário não for válido, exibe todas as casas
    casas = Casa.objects.all()
    context = {'casas': casas, 'form': form}
    return render(request, 'listagem_casas.html', context)



#Atualizar Casas Cadastradas
@login_required 
def atualizar_casa(request, casa_id):
    casa = get_object_or_404(Casa, pk=casa_id)

    if request.method == 'POST':
        casa.endereco = request.POST.get('endereco')
        casa.num_quarto = request.POST.get('num_quarto')
        casa.num_banheiro = request.POST.get('num_banheiro')
        casa.descricao = request.POST.get('descricao')
        casa.preco_total = request.POST.get('preco_total')
        casa.save()
        return redirect('detalhes_casa', casa_id=casa.id)  

    return render(request, 'atualizar_casa.html', {'casa': casa})


def redirecionar_pagamento(request, reserva_id):
    # Buscar a reserva pelo ID
    reserva = get_object_or_404(Reserva, id=reserva_id)

    # Passar os dados da reserva para a página de pagamento
    context = {
        'reserva': reserva,
        'casa': reserva.casa,  # Casa relacionada
    }

    # Renderizar a página interna de pagamentos
    return render(request, 'fazer_pagamentos.html', context)


