from django.urls import path
from . import views
from .views import MovimientosCreateView

urlpatterns = [
    path('', views.home, name='movimientos-home'),
    path('crear/', MovimientosCreateView.as_view(), name='movimientos-crear')
]
