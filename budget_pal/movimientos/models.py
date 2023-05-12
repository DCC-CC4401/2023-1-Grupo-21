from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

# Modelo para los movimientos de nuestro proyecto
class Movimientos(models.Model):
    nombre_movimiento = models.CharField(max_length=100)
    monto = models.IntegerField()
    categoria = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # Reescritura de str para mejor lectura al debugear
    def __str__(self):
        return self.usuario.username + " movio una cantidad de " + str(
            self.monto) + " con categoria " + self.categoria + "."
