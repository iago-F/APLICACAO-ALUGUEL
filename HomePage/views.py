# from django.shortcuts import render
# from Casa.models import Casa
# import random




from django.shortcuts import render
from Casa.models import Casa
import random
from random import sample

from django.shortcuts import render, get_object_or_404

def imagens_aleatorias(request):
    todas_as_casas = list(Casa.objects.all())
    casas_aleatorias = sample(todas_as_casas, min(len(todas_as_casas), 9))
    return render(request, 'HomePage.html', {'casas': casas_aleatorias})
    


def visualizar_detalhes_casa(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    
    context = {'casa': casa, 'usuario_cadastrou': casa.usuario}
    return render(request, 'DetalhesCasa.html', {'casa': casa})


















# def Pesquisa_Casa(request):
#     casas = Casa.objects.all()

#     if request.method == 'POST':
#         form = PesquisaCasaForm(request.POST)
#         if form.is_valid():
#             num_quartos = form.cleaned_data.get('num_quartos')
#             # Adicione outros critérios de pesquisa conforme necessário
#             if num_quartos:
#                 casas = casas.filter(num_quarto=num_quartos)

#     else:
#         form = PesquisaCasaForm()

#     return render(request, 'HomePage.html', {'casas': casas, 'form': form})