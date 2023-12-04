from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14)
    dt_nasc = models.DateField()
    instagram = models.CharField(max_length=30)
    telefone = models.CharField(max_length=14)
    def __str__(self):
        return self.user.username