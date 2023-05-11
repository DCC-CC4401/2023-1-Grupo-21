from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from .models import Movimientos


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        tabla = Movimientos.objects.filter(usuario=request.user)
        nueva_tabla = []
        for movimiento in tabla:
            if (movimiento.monto >= 0):
                nuevo_registro = {
                    'nombre_movimiento': movimiento.nombre_movimiento,
                    'categoria': movimiento.categoria,
                    'fecha': movimiento.fecha,
                    'usuario': movimiento.usuario,
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
        resultado = tabla.aggregate(Sum('monto'))
        suma_total = resultado['monto__sum']
        context = {
            'movimientos': nueva_tabla,
            'saldo' : suma_total
        }
        return render(request, 'home.html', context)
    else:
        return HttpResponseRedirect('/login/login/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/login/')


class MovimientosCreateView(LoginRequiredMixin, CreateView):
    model = Movimientos
    success_url = '/movimientos'
    fields = ['nombre_movimiento', 'monto', 'categoria', 'fecha']

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

