from django.shortcuts import render, redirect,get_object_or_404
from app1 import models
from decimal import Decimal

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

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if models.Usuario.objects.filter(email=email).exists():
            return redirect('registro')

        nuevo_usuario = models.Usuario(nombre_completo=nombre, email=email, contraseña=password)
        nuevo_usuario.save()
        
        return redirect('login')

    return render(request, 'registro.html')

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

def actualizar_cantidad(request, producto_id):
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})

        if str(producto_id) in carrito:
            carrito[str(producto_id)]['cantidad'] = nueva_cantidad
            carrito[str(producto_id)]['total'] = nueva_cantidad * carrito[str(producto_id)]['precio']
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

def direccionEnvio(request):
    return render(request, 'direccion_envio.html')

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
                total=producto_info['total'],
            )
            venta.save()

        request.session['carrito'] = {}

        return redirect('inicio')

    return render(request, 'pago.html')

def compra_exitosa(request):
    return render(request, 'compra_exitosa.html')

def historial_compras(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = models.Usuario.objects.get(id=usuario_id)
    compras = models.Venta.objects.filter(usuario=usuario).order_by('-fecha')

    # Agrupar compras por día y calcular el total
    compras_agrupadas = {}
    totales_por_dia = {}

    for compra in compras:
        fecha_formateada = compra.fecha.strftime('%Y-%m-%d')
        
        if fecha_formateada not in compras_agrupadas:
            compras_agrupadas[fecha_formateada] = []
            totales_por_dia[fecha_formateada] = Decimal('0.00')  # Asegúrate de que el total sea un Decimal

        compras_agrupadas[fecha_formateada].append(compra)
        totales_por_dia[fecha_formateada] += compra.total  # Acumulamos el total de cada compra

    return render(request, 'historialCompras.html', {
        'comprass': compras_agrupadas,
        'totales_por_dia': totales_por_dia
    })