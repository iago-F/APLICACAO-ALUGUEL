from django.db import models
from Casa.models import *
# Create your models here.

class Pagamento(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    numero_cartao = models.CharField(max_length=16)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"Pagamento para {self.casa} de {self.usuario} no valor de {self.valor}"
