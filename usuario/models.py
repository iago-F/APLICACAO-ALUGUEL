from django.db import models

class inquilino(models.Model):
    ID_inqui = models.IntegerField
    nome = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    cel_inqui = models.CharField(max_length=16)
    dt_cadastro = models.DateField
    CPF = models.CharField(max_length=13)

    def __str__(self) -> str:
        return self.nome
