from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from .models import Movimientos
from django.conf import settings


# Create your views here.
# Pagina principal
def home(request):
    # si el usuario fue autentificado, se procede a la pagina principal
    if request.user.is_authenticated:
        # se filtran los datos que pertenecen al usuario desde la base de datos
        tabla = Movimientos.objects.filter(usuario=request.user)
        # se crea la tabla que se va a mostrar en el html
        nueva_tabla = []
        # por cada movimiento de la tabla, se crea su equivalente en la nueva tabla que se va a mostrar en el 
        # html, manteniendo nombre_movimiento, categoria y fecha, agregando un tipo segun el monto (egreso si 
        # es negativo, ingreso de caso contrario) y colocando el monto como valor absoluto
        for movimiento in tabla:
            if (movimiento.monto >= 0):
                nuevo_registro = {
                    'nombre_movimiento': movimiento.nombre_movimiento,
                    'categoria': movimiento.categoria,
                    'fecha': movimiento.fecha,
                    'monto': movimiento.monto,
                    'tipo': 'Ingreso'
                }
            else:
                nuevo_registro = {
                    'nombre_movimiento': movimiento.nombre_movimiento,
                    'categoria': movimiento.categoria,
                    'fecha': movimiento.fecha,
                    'monto': -movimiento.monto,
                    'tipo': 'Egreso'
                }
            nueva_tabla.append(nuevo_registro)
        # calculo la suma de todos los montos de la tabla original (para mostrar el saldo disponible)
        resultado = tabla.aggregate(Sum('monto'))
        suma_total = resultado['monto__sum']
        # el saldo y los movimientos del usuario (de la nueva tabla) los pongo en el contexto para visualizarse
        context = {
            'movimientos': nueva_tabla,
            'saldo' : suma_total
        }
        return render(request, 'home.html', context)
    else:
        # si el usuario no esta autentificado, se manda al login para que ingrese su usuario
        return HttpResponseRedirect(settings.LOGIN_URL)


# Vista para desloguearse (usado en el boton de logout)
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


# Clase view para la pestaña de ingresar movimientos
class MovimientosCreateView(LoginRequiredMixin, CreateView):
    model = Movimientos
    success_url = '/movimientos'
    fields = ['nombre_movimiento', 'monto', 'categoria', 'fecha']

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

