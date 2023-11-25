from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Casa(models.Model):
    endereco = models.CharField(max_length=200)
    num_quarto = models.IntegerField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    num_banheiro = models.IntegerField()
    descricao = models.TextField()
    area = models.TextField()
    imagem = models.ImageField(upload_to='imagens_casas/', blank=True, null=True)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, default=None)

    def save(self, *args, **kwargs):
        if not self.usuario_id:
            self.usuario = kwargs.pop('user', None)
        super(Casa, self).save(*args, **kwargs)

    def __str__(self):
        return f"Casa em {self.endereco}"
