from django.shortcuts import render
from .models import Movimientos

# Create your views here.
def home(request):
    context = {
        'movimientos': Movimientos.objects.all()
    }
    return render(request, 'home.html', context)