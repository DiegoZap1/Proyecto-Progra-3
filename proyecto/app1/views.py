from django.shortcuts import render, redirect,get_object_or_404
from app1 import models

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = models.Usuario.objects.get(email=email, contraseña=password)
            request.session['usuario_id'] = usuario.id
            return redirect('inicio')
        except models.Usuario.DoesNotExist:
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

        cantidad = int(request.POST.get('cantidad',1))

        if str(producto_id) not in carrito:
            carrito[str(producto_id)]={
                'nombre':producto.nombre,
                'precio':float(producto.precio),
                'cantidad':cantidad,
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
    total_carrito = sum(producto['total'] for producto in carrito.values())
    return render(request, 'carrito.html',{'carrito':carrito,'total_carrito':total_carrito})

def cuenta(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    
    usuario = models.Usuario.objects.get(id=usuario_id)
    return render(request, 'cuenta.html',{'usuario':usuario})

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
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = models.Usuario.objects.get(id=usuario_id)
    carrito = request.session.get('carrito', {})

    if request.method == 'POST':
        for producto_id, producto_info in carrito.items():
            producto = models.Producto.objects.get(id=producto_id)
            venta = models.Venta(
                usuario=usuario,
                producto=producto,
                cantidad=producto_info['cantidad'],
                precio=producto_info['precio'],
                total=producto_info['total'],
                fecha=producto_info['fecha'],
            )
        venta.save()
        return redirect('inicio')

    return render(request, 'pago.html')


def historial_compras(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = models.Usuario.objects.get(id=usuario_id)
    compras = models.Venta.objects.filter(usuario=usuario)

    compras_agrupadas = {}
    for compra in compras:
        if compra.fecha not in compras_agrupadas:
            compras_agrupadas[compra.fecha] = []
        compras_agrupadas[compra.fecha].append(compra)

    return render(request, 'historialCompras.html', {'comprass': compras_agrupadas})