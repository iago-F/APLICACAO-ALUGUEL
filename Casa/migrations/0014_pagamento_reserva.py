# Generated by Django 4.2.5 on 2023-12-01 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Casa', '0013_casa_valor_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='reserva',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Casa.reserva'),
        ),
    ]
