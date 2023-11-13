from django.shortcuts import render
from .models import Casa
from .forms import CasaForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
        
@login_required
def cadastrarCasa(request):
    if request.method == 'POST':
        form = CasaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            

        
    else:
        form = CasaForm()

    return render(request, 'CadastrarCasa.html',{'form':form})

