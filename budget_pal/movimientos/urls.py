from django.urls import path
from . import views
from .views import MovimientosCreateView

# Urls para cada pagina
urlpatterns = [
    path('', views.home, name='movimientos-home'),
    path('crear/', MovimientosCreateView.as_view(), name='movimientos-crear'),
    path('logout',views.logout_user, name='logout'),
    path('delete/<int:id>/', views.delete_movimiento, name='delete-movimiento'),
]
