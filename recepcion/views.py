from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from ordenes.models import OrdenCompra, ItemOrdenCompra
from productos.models import Producto  # Ajusta si tu modelo está en otra app
from usuarios.models import Usuario
from recepcion.models import Faltante

#Recepción (pendiente)
@login_required
def inicio_recepcion(request):
    ordenes_pendientes = OrdenCompra.objects.filter(estado__in=['Emitida', 'Aprobada'])
    return render(request, 'recepcion/inicio.html', {'ordenes': ordenes_pendientes})

@login_required
def detalle_orden_recepcion(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    items = ItemOrdenCompra.objects.filter(orden=orden).select_related('producto')
    return render(request, 'recepcion/detalle_orden.html', {
        'orden': orden,
        'items': items
    })

@login_required
def confirmar_recepcion(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)

    if orden.estado not in ['Emitida', 'Aprobada']:
        messages.error(request, 'La orden no está en un estado válido para recepción.')
        return redirect('detalle_recepcion', orden_id=orden.id)

    items = ItemOrdenCompra.objects.filter(orden=orden).select_related('producto')
    for item in items:
        producto = item.producto
        producto.stock += item.cantidad
        producto.save()

    orden.estado = 'Recibida'
    orden.save()

    messages.success(request, 'Recepción confirmada y stock actualizado.')
    return redirect('recepcion')

@login_required
def reportar_faltante(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        try:
            cantidad_recibida = int(request.POST.get('cantidad_recibida'))
        except (TypeError, ValueError):
            messages.error(request, "Cantidad recibida inválida.")
            return redirect('reportar_faltante', orden_id=orden.id)

        producto = get_object_or_404(Producto, pk=producto_id)
        item = get_object_or_404(ItemOrdenCompra, orden=orden, producto=producto)

        if cantidad_recibida > item.cantidad:
            messages.error(request, "La cantidad recibida no puede ser mayor que la solicitada.")
            return redirect('reportar_faltante', orden_id=orden.id)

        faltante = Faltante.objects.create(
            orden=orden,
            producto=producto,
            cantidad_solicitada=item.cantidad,
            cantidad_recibida=cantidad_recibida,
            reportado_por=request.user,
            fecha_reporte=timezone.now()
        )

        orden.estado = 'Faltante'
        orden.save()

        messages.success(request, "Faltante registrado correctamente.")
        return redirect('recepcion')

    productos_en_orden = ItemOrdenCompra.objects.filter(orden=orden).select_related('producto')
    return render(request, 'recepcion/reportar_faltante.html', {
        'orden': orden,
        'productos_en_orden': productos_en_orden
    })

#Recibidos

@login_required
def recibidos(request):
    ordenes_recibidas = OrdenCompra.objects.filter(estado__in=['Recibida'])
    return render(request, 'recepcion/recibidos.html', {'ordenes': ordenes_recibidas})

@login_required
def detalle_recibido(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    items = ItemOrdenCompra.objects.filter(orden=orden).select_related('producto')
    return render(request, 'recepcion/detalle_recibido.html', {
        'orden': orden,
        'items': items
    })

#faltantes
@login_required
def faltantes(request):
    ordenes_faltantes = OrdenCompra.objects.filter(estado__in=['Faltante'])
    return render(request, 'recepcion/faltantes.html', {'ordenes': ordenes_faltantes})

@login_required
def detalle_faltante(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    items = ItemOrdenCompra.objects.filter(orden=orden).select_related('producto')
    return render(request, 'recepcion/detalle_faltante.html', {
        'orden': orden,
        'items': items
    })

