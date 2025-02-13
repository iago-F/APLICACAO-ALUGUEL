# from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# import datetime
#
#
# class Casa(models.Model):
#     endereco = models.CharField(max_length=200)
#     num_quarto = models.IntegerField()
#     preco_total = models.DecimalField(max_digits=10, decimal_places=2)
#     num_banheiro = models.IntegerField()
#     descricao = models.TextField()
#     area = models.TextField()
#     imagem = models.ImageField(upload_to='imagens_casas/', blank=True, null=True)
#     usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, default=    None)
#     usuario_cadastrou = models.ForeignKey(User, on_delete=models.CASCADE, related_name='casas_cadastradas', null=True, blank=True)
#     valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#
#     def save(self, *args, **kwargs):
#         if not self.usuario_id:
#             self.usuario = kwargs.pop('user', None)
#         super(Casa, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return f"Casa em {self.endereco}"
#
#
#
# class Reserva(models.Model):
#     casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
#     usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     data_reserva = models.DateTimeField(auto_now_add=True)
#
#     data_final = models.DateField(default=datetime.date.today)
#
#     def __str__(self):
#         return f"Reserva da casa em {self.casa.endereco} por {self.usuario.username}"
#
#
#
#
# def valor_pago(self):
#     """
#     Soma todos os pagamentos referentes a esta casa.
#     """
#     from pagamento.models import Pagamento  # Import dentro do método, para evitar import circular
#     total_pagamentos = Pagamento.objects.filter(casa=self).aggregate(Sum('valor'))['valor__sum']
#     if total_pagamentos is None:
#         total_pagamentos = 0
#     return total_pagamentos
#
#
# def valor_restante(self):
#     """
#     Retorna o quanto ainda falta pagar (preco_total - valor_pago).
#     """
#     return self.preco_total - (self.valor_pago or 0)




from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime


class Casa(models.Model):
    endereco = models.CharField(max_length=200)
    num_quarto = models.IntegerField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    num_banheiro = models.IntegerField()
    descricao = models.TextField()
    area = models.TextField()
    imagem = models.ImageField(upload_to='imagens_casas/', blank=True, null=True)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, default=None)
    usuario_cadastrou = models.ForeignKey(User, on_delete=models.CASCADE, related_name='casas_cadastradas', null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        if not self.usuario_id:
            self.usuario = kwargs.pop('user', None)
        super(Casa, self).save(*args, **kwargs)

    def __str__(self):
        return f"Casa em {self.endereco}"

    @property
    def valor_pago(self):
        """
        Soma todos os pagamentos feitos para essa casa.
        """
        from pagamento.models import Pagamento  # Evita import circular
        total = Pagamento.objects.filter(casa=self).aggregate(Sum('valor'))['valor__sum']
        return total if total else 0

    @property
    def valor_restante(self):
        """
        Calcula o valor restante a pagar na casa.
        """
        return self.preco_total - self.valor_pago


class Reserva(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)
    data_final = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"Reserva da casa em {self.casa.endereco} por {self.usuario.username}"
