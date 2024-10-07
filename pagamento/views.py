from django.shortcuts import render
from .models import Pagamento
from Casa.models import Reserva
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
# Create your views here.




@login_required
def realizar_pagamento(request, reserva_id):
    # Busca a reserva pelo ID
    minha_reserva = get_object_or_404(Reserva, id=reserva_id)



    # Inicializa a variável para mensagens de exceção
    pagamento_excecao = None

    # Se o método for POST, processa o pagamento
    if request.method == 'POST':
        numero_cartao = request.POST.get('numero_cartao')  # Captura o número do cartão
        valor = float(request.POST.get('valor', minha_reserva.casa.preco_total))  # Captura o valor do pagamento

        # Calcula a soma de todos os pagamentos feitos para essa reserva
        total_pagamentos_ja_feitos = Pagamento.objects.filter(reserva=minha_reserva).aggregate(Sum('valor'))[
                                         'valor__sum'] or 0
        valor_restante = minha_reserva.casa.preco_total - total_pagamentos_ja_feitos

        # Verifica se o novo pagamento ultrapassa o valor total da casa
        if valor > valor_restante:
            pagamento_excecao = f"O pagamento excede o valor restante da casa. Você ainda pode pagar: {valor_restante:.2f}."
            messages.error(request, pagamento_excecao)
            return render(request, 'fazer_pagamentos.html',
                          {'reserva': minha_reserva, 'pagamento_excecao': pagamento_excecao})

        # Captura o usuário logado
        usuario_logado = request.user

        # Cria o pagamento se estiver dentro do limite
        Pagamento.objects.create(
            casa=minha_reserva.casa,
            usuario=usuario_logado,  # Registra o usuário logado
            numero_cartao=numero_cartao,
            valor=valor,
            reserva=minha_reserva
        )

        # Mensagem de sucesso
        pagamento_sucesso = f"Pagamento processado com sucesso!"
        messages.success(request, pagamento_sucesso)
        return render(request, 'fazer_pagamentos.html', {'reserva': minha_reserva,
                      'pagamento_sucesso': pagamento_sucesso})

    # Se o método for GET, renderiza o template do formulário de pagamento
    return render(request, 'fazer_pagamentos.html', {'reserva': minha_reserva})
