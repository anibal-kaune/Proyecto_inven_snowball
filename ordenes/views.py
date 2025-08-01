from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdenCompra, ItemOrdenCompra
from productos.models import Producto
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from xhtml2pdf import pisa
import tempfile
from django.template.loader import get_template

@login_required
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.all()
    return render(request, 'ordenes/lista_ordenes.html', {'ordenes': ordenes})


@login_required
@transaction.atomic
def crear_orden(request):
    productos = Producto.objects.all()

    if request.method == 'POST':
        productos_ids = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')

        if not productos_ids or not cantidades or len(productos_ids) != len(cantidades):
            return render(request, 'ordenes/crear_orden.html', {
                'productos': productos,
                'error': 'Debe agregar al menos un producto con cantidad válida.'
            })

        orden = OrdenCompra.objects.create(usuario=request.user)
        productos_agregados = set()

        for producto_id, cantidad_str in zip(productos_ids, cantidades):
            if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
                continue

            if producto_id in productos_agregados:
                continue

            productos_agregados.add(producto_id)
            producto = get_object_or_404(Producto, id=producto_id)
            ItemOrdenCompra.objects.create(
                orden=orden,
                producto=producto,
                cantidad=int(cantidad_str)
            )

        return redirect('detalle_orden', orden.numero)

    return render(request, 'ordenes/crear_orden.html', {'productos': productos})


@login_required
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, numero=orden_id)
    estados_editables = []
    if request.user.rol == 'supervisor':
        estados_editables = [
            ('Emitida', 'Emitida'),
            ('Aprobada', 'Aprobada'),
            ('Cancelada', 'Cancelada'),
        ]
    return render(request, 'ordenes/detalle_orden.html', {'orden': orden, 'estados_editables': estados_editables,})

@login_required
def cambiar_estado_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, numero=orden_id)

    if not request.user.rol == 'supervisor':  # Usamos el campo del modelo Usuario
        return HttpResponseForbidden("No tienes permisos para cambiar el estado.")

    ESTADOS_PERMITIDOS = ['Emitida', 'Aprobada', 'Cancelada']

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ESTADOS_PERMITIDOS:
            orden.estado = nuevo_estado
            orden.save()
            messages.success(request, f'Estado actualizado a "{nuevo_estado}".')
        else:
            messages.error(request, "Estado no permitido.")

    return redirect('lista_ordenes')

#generar PDF
def generar_pdf_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    template = get_template('ordenes/pdf_orden.html')
    html = template.render({'orden': orden})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Orden_{orden.numero}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response