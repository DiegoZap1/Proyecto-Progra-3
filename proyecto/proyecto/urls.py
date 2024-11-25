from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login, name='login'),
    path('registro/', views.registro, name="registro"),
    path('',views.inicio, name='inicio'),
    path('catalogo/',views.catalogo, name="catalogo"),
    path('cuenta/', views.cuenta, name="cuenta"),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('carrito/',views.carrito, name="carrito"),
    path('producto/<int:producto_id>/',views.producto, name="producto"),
    path('pago/',views.pago, name='pago'),
    path('historial_compras/', views.historial_compras, name='historial_compras'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)