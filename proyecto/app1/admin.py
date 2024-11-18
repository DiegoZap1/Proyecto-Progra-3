from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Usuario)
admin.site.register(models.Producto)
admin.site.register(models.Venta)
admin.site.register(models.HistorialCompra)