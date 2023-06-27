from django.urls import path
from . import views
from .views import MovimientosCreateView, MovimientosUpdateView, MovimientosDeleteView

# Urls para cada pagina
urlpatterns = [
    path('', views.home, name='movimientos-home'),
    path('crear/', MovimientosCreateView.as_view(), name='movimientos-crear'),
    path('update/<int:pk>/', MovimientosUpdateView.as_view(), name='movimientos-update'),
    path('logout', views.logout_user, name='logout'),
    path('delete/<int:pk>/', MovimientosDeleteView.as_view(), name='movimientos-delete'),
    path('filtro/', views.filtro, name='movimientos-filtro')
]
