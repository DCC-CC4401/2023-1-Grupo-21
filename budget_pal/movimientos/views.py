from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.db.models import Sum

from .models import Movimientos


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        tabla = Movimientos.objects.filter(usuario=request.user)
        resultado = tabla.aggregate(Sum('monto'))
        suma_total = resultado['monto__sum']
        context = {
            'movimientos': tabla,
            'saldo' : suma_total
        }
        return render(request, 'home.html', context)
    else:
        return HttpResponseRedirect('/login/login/')

def logout_user(request):
   logout(request)
   return HttpResponseRedirect('/login/login/')


class MovimientosCreateView(CreateView):
    model = Movimientos
    success_url = '/movimientos'
    fields = ['nombre_movimiento', 'monto', 'categoria', 'fecha']

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
