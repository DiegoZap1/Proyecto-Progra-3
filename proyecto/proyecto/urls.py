from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login, name='login'),
    path('registro/', views.registro, name="registro"),
    path('inicio/',views.inicio, name='inicio'),
    path('catalogo/',views.catalogo, name="catalogo"),
    path('cuenta/', views.cuenta, name="cuenta"),
    path('carrito/',views.carrito, name="carrito"),
]