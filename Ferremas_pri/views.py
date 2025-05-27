from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from  .api import Mindicador
from .models import * 
from .serializers import ProductoSerializer
from django.http import JsonResponse
from django.template.loader import render_to_string
from .transbank_integration import issue_payment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import traceback


def get_dolar_price(request):
    mindicador = Mindicador('dolar', 2024)
    dolar_price = mindicador.get_dolar_price()
    return JsonResponse({'dolar_price': dolar_price})

def testeo(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def base(request):
    context = {}
    return render(request, 'ferremas_pri/base.html', context)

def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'ferremas_pri/inicio.html', {'productos': productos})

def pagar(request):
    return render(request, 'ferremas_pri/pagar.html')

#                                                                           Cosas de Productos ~
def lista_productos(request):
    context = {}
    return render(request, 'ferremas_pri/lista_productos.html',context)

class ProductoListCreate(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


#                                                                               Cosas Carrito ~

# ejemplo de vista
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    for item_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=item_id)
        total_item = producto.precio * cantidad
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'total': total_item
        })
        total += total_item
    return render(request, 'Ferremas_pri/ver_carrito.html', {'items': items, 'total': total})




def agregar_al_carrito(request, producto_id):
    # Solo aceptar Ajax
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)
    
    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

    # Obtener carrito de la sesión (o crear si no existe)
    carrito = request.session.get('carrito', {})

    # Incrementar cantidad del producto o agregarlo
    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1

    # Guardar carrito en sesión
    request.session['carrito'] = carrito

    # Contar total de items
    total_items = sum(carrito.values())

    return JsonResponse({'total_items': total_items})


def eliminar_del_carrito(request, item_id):
    item = ItemCarrito.objects.get(pk=item_id)
    item.delete()
    return redirect('ver_carrito')


def limpiar_carrito(request):
    ItemCarrito.objects.filter(user=request.user).delete()
    return redirect('ver_carrito')


def obtener_contenido_carrito(request):
    items = ItemCarrito.objects.filter(user=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)
    html = render_to_string('Ferremas_pri/partials/carrito_contenido.html', {'items': items, 'total': total})
    return JsonResponse({'html': html})

#                                                              Integrando la API de Transbank ~
@csrf_exempt
@require_POST
def realizar_pago(request):
    try:
        data = json.loads(request.body)

        commerce_id = data.get('commerceId')
        commerce_payment_id = data.get('commercePaymentId')
        processor_payment_id = data.get('processorPaymentId')
        service_id = data.get('serviceId')
        client_id = data.get('clientId')

        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        # Obtener items del carrito según session_id
        items = ItemCarrito.objects.filter(session_id=session_key)
        amount = sum(item.producto.precio * item.cantidad for item in items)

        # Aquí va la llamada a tu API de pago
        response = issue_payment(
            commerce_id,
            commerce_payment_id,
            processor_payment_id,
            service_id,
            client_id,
            amount=amount
        )

        # Si el pago fue autorizado, eliminar los items del carrito
        if response.get("status") == "AUTHORIZED":
            items.delete()

        return JsonResponse(response)
    except Exception as e:
        print("Error en realizar_pago:", e)
        traceback.print_exc()
        return JsonResponse({"status": "ERROR", "message": str(e)}, status=500)