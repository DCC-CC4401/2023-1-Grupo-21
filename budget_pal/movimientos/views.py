import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.conf import settings
import datetime
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from django.db.models.functions import ExtractMonth
from .models import Movimientos
from .models import Filtro
from django.conf import settings


# Create your views here.
# Pagina principal
def home(request):
    # si el usuario fue autentificado, se procede a la pagina principal
    url_movimientos = "movimientos-home"
    if request.user.is_authenticated:
        # se filtran los datos que pertenecen al usuario desde la base de datos
        movimientos = Movimientos.objects.filter(usuario=request.user)

        #se calcula el saldo del usuario
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

        # determina que sort se esta haciendo, si no se hace ninguno se devuelve None
        sort = request.GET.get('sort')
        # ordeno segun el sort que se selecciono
        if sort:
            movimientos = movimientos.order_by(sort)

        fecha_actual = datetime.date.today()
        ingresos_por_mes = Movimientos.objects.filter(usuario=request.user, tipo=Movimientos.TipoMovimiento.INGRESO, fecha__year=fecha_actual.year).annotate(mes=ExtractMonth('fecha')).values('mes').annotate(total=Sum('monto'))
        egresos_por_mes = Movimientos.objects.filter(usuario=request.user, tipo=Movimientos.TipoMovimiento.EGRESO, fecha__year=fecha_actual.year).annotate(mes=ExtractMonth('fecha')).values('mes').annotate(total=Sum('monto'))

        meses = [datetime.date(1, i, 1).strftime('%B') for i in range(1, 13)]

        # Crear listas separadas para los ingresos y egresos
        ingresos = [0] * len(meses)
        egresos = [0] * len(meses)

        # Asignar los montos a las listas correspondientes
        for ingreso in ingresos_por_mes:
            mes = ingreso['mes'] - 1  # Restar 1 porque los índices de la lista comienzan desde 0
            ingresos[mes] = ingreso['total']

        for egreso in egresos_por_mes:
            mes = egreso['mes'] - 1
            egresos[mes] = egreso['total']

        # Crear el gráfico de barras dobles
        x = np.arange(len(meses))
        width = 0.35

        fig, ax = plt.subplots()
        fig.set_size_inches(11, 5)
        ax.bar(x - width/2, ingresos, width, label='Ingresos')
        ax.bar(x + width/2, egresos, width, label='Egresos')

        ax.set_xlabel('Meses')
        ax.set_ylabel('Monto')
        ax.set_title('Ingresos y Egresos por Mes (' + str(fecha_actual.year) + ')')
        ax.set_xticks(x)
        ax.set_xticklabels(meses,rotation=25)
        ax.legend()

        # Guardar el gráfico en una variable BytesIO
        grafico_bytes = BytesIO()
        plt.savefig(grafico_bytes, format='png')
        plt.close()

        # Convertir los bytes a una cadena base64 para pasarla al contexto del template
        grafico_base64 = base64.b64encode(grafico_bytes.getvalue()).decode('utf-8')

        # el saldo, el grafico y los movimientos del usuario (de la nueva tabla) los pongo en el contexto para visualizarse
        context = {
            'movimientos': movimientos,
            'saldo': monto_total,
            'url_movimientos': url_movimientos,
            'grafico_base64': grafico_base64,
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
    url_movimientos = "movimientos-filtro"
    if request.user.is_authenticated:
        # se filtran los datos que pertenecen al usuario desde la base de datos
        movimientos = Movimientos.objects.filter(usuario=request.user)
        
        # veo el ultimo filtro del usuario o en caso contrario creo un filtro
        usuario = request.user
        filtro_usuario, create = Filtro.objects.get_or_create(usuario=usuario)

        # si estamos filtrando, se actualiza la tabla de ultimos datos filtrados del usuario
        if 'filtro' in request.GET:
            filtro_usuario.tipo = request.GET.get('Tipo')
            filtro_usuario.categoria = request.GET.get('Categoria')
            # ya que filtro_usuario.fecha_inicial no acepta None se coloca como tiempo minimo al ordenar el año 1000
            fecha_inicial = request.GET.get('Fecha_inicial')
            if fecha_inicial:
                filtro_usuario.fecha_inicial = request.GET.get('Fecha_inicial')
            else:
                filtro_usuario.fecha_inicial = datetime.datetime(1000, 1, 1)
            # ya que filtro_usuario.fecha_final no aecpta None se coloca como tiempo maximo al ordenar el año 9999
            fecha_final = request.GET.get('Fecha_final')
            if fecha_final:
                filtro_usuario.fecha_final = request.GET.get('Fecha_final')
            else:
                filtro_usuario.fecha_final = datetime.datetime(9999, 12, 1)
            filtro_usuario.save()
        # si estamos reiniciando, se reinicia a su valor inical la tabla de ultimos datos filtrados
        if ("reiniciar" in request.GET or create):
            filtro_usuario.tipo = ""
            filtro_usuario.categoria = ""
            filtro_usuario.fecha_inicial = datetime.datetime(1000, 1, 1)
            filtro_usuario.fecha_final = datetime.datetime(9999, 12, 1)
            filtro_usuario.save()
        # decimos los valores del filtro actual
        filtro_tipo = filtro_usuario.tipo
        filtro_categoria = filtro_usuario.categoria
        filtro_fecha_inicial = filtro_usuario.fecha_inicial
        filtro_fecha_final = filtro_usuario.fecha_final

        #se aplican los distintos filtros a la tabla
        if filtro_categoria:
            movimientos = movimientos.filter(categoria__icontains=filtro_categoria)
        if filtro_tipo:
            movimientos = movimientos.filter(tipo__icontains=filtro_tipo)
        movimientos =movimientos.filter(fecha__gt=filtro_fecha_inicial)
        movimientos =movimientos.filter(fecha__lt=filtro_fecha_final)
        
        # vemos a que atributo de la tabla se le quiere hacer sort
        sort = request.GET.get('sort')
        # si se quiere hacer un sort, se aplica el sort al atributo correspondiente en la tabla
        if sort:
            movimientos = movimientos.order_by(sort)


        # el saldo y los movimientos del usuario (de la nueva tabla) los pongo en el contexto para visualizarse
        context = {
            'movimientos': movimientos,
            'url_movimientos': url_movimientos
        }
        return render(request, 'movimientos/filtros.html', context)
    else:
        # si el usuario no esta autentificado, se manda al login para que ingrese su usuario
        return HttpResponseRedirect(settings.LOGIN_URL)
