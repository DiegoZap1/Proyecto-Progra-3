from django.db import models

# Modelo para los usuarios
class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)

# Modelo para los productos
class Producto(models.Model):
    imagen = models.ImageField(upload_to='productos/')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=1000)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

# Modelo para las ventas
class Venta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)