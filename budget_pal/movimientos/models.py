from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

# Modelo para los movimientos de nuestro proyecto
class Movimientos(models.Model):
    class TipoMovimiento(models.TextChoices):
        INGRESO = "ingreso", "Ingreso"
        EGRESO = "egreso", "Egreso"
    nombre_movimiento = models.CharField(max_length=100, help_text="Nombre del movimiento, maximo 100 caracteres.")
    monto = models.IntegerField(help_text="El monto debe ser un entero positivo.")
    categoria = models.CharField(max_length=100, help_text="Ponga cualquier categoria")
    fecha = models.DateTimeField(default=timezone.now, help_text="La fecha actual, fecha de creacion del movimiento.")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=10, 
        choices=TipoMovimiento.choices,
        default=TipoMovimiento.INGRESO,
        help_text="Tipo de movimiento."
    )

    # Reescritura de str para mejor lectura al debugear
    def __str__(self):
        return self.usuario.username + " movio una cantidad de " + str(
            self.monto) + " con categoria " + self.categoria + " y de tipo " + self.tipo + "."
