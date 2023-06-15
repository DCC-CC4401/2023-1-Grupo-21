from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import JsonResponse

from .models import Movimientos
from django.conf import settings


# Create your views here.
# Pagina principal
def home(request):
    # si el usuario fue autentificado, se procede a la pagina principal
    if request.user.is_authenticated:
        # se filtran los datos que pertenecen al usuario desde la base de datos
        movimientos = Movimientos.objects.filter(usuario=request.user)
        ingresos = Movimientos.objects.filter(usuario=request.user, tipo=Movimientos.TipoMovimiento.INGRESO).aggregate(
            Sum('monto'))
        egresos = Movimientos.objects.filter(usuario=request.user, tipo=Movimientos.TipoMovimiento.EGRESO).aggregate(
            Sum('monto'))
        monto_egresos = egresos['monto__sum']
        monto_ingresos = ingresos['monto__sum']

        if monto_egresos == None:
            monto_egresos = 0
        if monto_ingresos == None:
            monto_ingresos = 0

        monto_total = monto_ingresos - monto_egresos

        # el saldo y los movimientos del usuario (de la nueva tabla) los pongo en el contexto para visualizarse
        context = {
            'movimientos': movimientos,
            'saldo': monto_total
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
    fields = ['nombre_movimiento', 'tipo', 'monto', 'categoria', 'fecha']

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


# Clase view para la pestaña de updatear movimientos
class MovimientosUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movimientos
    success_url = '/movimientos'
    fields = ['nombre_movimiento', 'tipo', 'monto', 'categoria', 'fecha']

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def test_func(self):
        movimiento = self.get_object()
        return self.request.user.id == movimiento.usuario_id


class MovimientosDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movimientos
    success_url = '/movimientos'

    def test_func(self):
        movimiento = self.get_object()
        return self.request.user.id == movimiento.usuario_id


def filtro(request):
    # si el usuario fue autentificado, se procede a la pagina principal
    if request.user.is_authenticated:
        # se filtran los datos que pertenecen al usuario desde la base de datos
        movimientos = Movimientos.objects.filter(usuario=request.user)

        # el saldo y los movimientos del usuario (de la nueva tabla) los pongo en el contexto para visualizarse
        context = {
            'movimientos': movimientos,
        }
        return render(request, 'movimientos/filtros.html', context)
    else:
        # si el usuario no esta autentificado, se manda al login para que ingrese su usuario
        return HttpResponseRedirect(settings.LOGIN_URL)


def filtrar(request):
    filtro_tipo = request.POST.get('Tipo')
    filtro_categoria = request.POST.get('Categoria')
    filtro_fecha_inicial = request.POST.get('Fecha_inicial')
    filtro_fecha_final = request.POST.get('Fecha_final')

    # se filtran los datos que pertenecen al usuario desde la base de datos
    movimientos = Movimientos.objects.filter(usuario=request.user, categoria__icontains=filtro_categoria)

    # el saldo y los movimientos del usuario (de la nueva tabla) los pongo en el contexto para visualizarse
    context = {
        'movimientos': movimientos,
    }
    return render(request, 'movimientos/tabla.html', context)
    # return JsonResponse({'tabla_html': tabla_html})
