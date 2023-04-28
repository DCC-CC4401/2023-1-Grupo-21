from django.shortcuts import render
from django.views.generic import CreateView

from .models import Movimientos


# Create your views here.
def home(request):
    context = {
        'movimientos': Movimientos.objects.all()
    }
    return render(request, 'home.html', context)


class MovimientosCreateView(CreateView):
    model = Movimientos
    success_url = '/movimientos'
    fields = ['nombre_movimiento', 'monto', 'categoria', 'fecha']

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
