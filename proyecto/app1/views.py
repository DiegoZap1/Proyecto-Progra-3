from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from app1 import models

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = models.Usuario.objects.get(email=email, contraseña=password)
            return redirect('inicio')
        except models.Usuario.DoesNotExist:
            messages.error(request, 'El usuario o la contraseña son incorrectos.')
            return redirect('login')
        
    return render(request, 'login.html')

def inicio(request):
    return render(request, 'inicio.html')

def catalogo(request):
    productos = models.Producto.objects.all()
    return render(request, 'catalogo.html',
                  {'productos':productos})

def producto(request,producto_id):
    producto = get_object_or_404(models.Producto,id=producto_id)

    if request.method == 'POST':
        carrito = request.session.get('carrito',{})

        if str(producto_id) not in carrito:
            carrito[str(producto_id)]={
                'nombre':producto.nombre,
                'precio':float(producto.precio),
                'cantidad':1,
                'total':float(producto.precio),
            }
        else:
            carrito[str(producto_id)]['cantidad'] += 1
            carrito[str(producto_id)]['total'] = carrito[str(producto_id)]['cantidad'] * carrito[str(producto_id)]['precio']
        
        request.session['carrito'] = carrito
        return redirect('carrito')  

    return render(request, 'producto.html',{'producto':producto})

def eliminar_producto(request, producto_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        if str(producto_id) in carrito:
            del carrito[str(producto_id)]
            request.session['carrito'] = carrito
        return redirect('carrito')

def carrito(request):
    carrito = request.session.get('carrito', {})
    return render(request, 'carrito.html',{'carrito':carrito})

def cuenta(request):
    return render(request, 'cuenta.html')

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Verificar si el email ya está registrado
        if models.Usuario.objects.filter(email=email).exists():
            return redirect('register')  # Redirige al formulario de registro si hay un error

        # Crear y guardar el nuevo usuario
        nuevo_usuario = models.Usuario(nombre_completo=nombre, email=email, contraseña=password)
        nuevo_usuario.save()
        
        return redirect('login')  # Redirige a la página de inicio de sesión

    return render(request, 'registro.html')

def pago(request):
    return render(request, 'pago.html')