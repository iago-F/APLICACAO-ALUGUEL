from django.shortcuts import render
from Casa.models import Casa
import random

# mostar as casas que estão cadastradas no banco de forma aleatoria
def Casas_random(request):
    casas = Casa.objects.all().order_by('?')[:3]  # Altere o número 3 para o número desejado de casas a serem exibidas
    return render(request, 'HomePage.html', {'casas': casas})
