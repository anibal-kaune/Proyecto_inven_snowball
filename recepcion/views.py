from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from ordenes.models import OrdenCompra, ItemOrdenCompra
from productos.models import Producto  # Ajusta si tu modelo está en otra app
from usuarios.models import Usuario
from recepcion.models import Faltante
from django.http import HttpResponseForbidden, HttpResponse
from xhtml2pdf import pisa
import tempfile
from django.template.loader import get_template
from io import BytesIO

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
        productos_ids = request.POST.getlist('producto_id[]')
        cantidades_recibidas = request.POST.getlist('cantidad_recibida[]')

        productos_con_faltante = set()

        for producto_id, cant_recibida in zip(productos_ids, cantidades_recibidas):
            producto = get_object_or_404(Producto, pk=producto_id)
            item = get_object_or_404(ItemOrdenCompra, orden=orden, producto=producto)

            cant_recibida = int(cant_recibida)
            cant_solicitada = item.cantidad

            if cant_recibida < cant_solicitada:
                # Crear registro de faltante
                Faltante.objects.create(
                    orden=orden,
                    producto=producto,
                    cantidad_solicitada=cant_solicitada,
                    cantidad_recibida=cant_recibida,
                    reportado_por=request.user,
                    fecha_reporte=timezone.now()
                )
                productos_con_faltante.add(producto.id)

            # Siempre se suma lo recibido al stock
            producto.stock += cant_recibida
            producto.save()

        # Procesar productos que no fueron reportados como faltantes (recibidos completos)
        items_orden = ItemOrdenCompra.objects.filter(orden=orden).select_related('producto')
        for item in items_orden:
            if item.producto.id not in productos_con_faltante:
                item.producto.stock += item.cantidad
                item.producto.save()

        orden.estado = 'Faltante'
        orden.save()

        messages.success(request, "Faltantes registrados y stock actualizado.")
        return redirect('faltantes')

    productos_en_orden = ItemOrdenCompra.objects.filter(orden=orden).select_related('producto')
    return render(request, 'recepcion/reportar_faltante.html', {
        'orden': orden,
        'productos_en_orden': productos_en_orden
    })

#generar PDF
def generar_pdf_recibido(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    template = get_template('recepcion/pdf_recibido.html')
    html = template.render({'orden': orden})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Orden_{orden.numero}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

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

#generar PDF
def generar_pdf_recibido(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    template = get_template('recepcion/pdf_recibido.html')
    html = template.render({'orden': orden})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Orden_{orden.numero}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

#faltantes
@login_required
def faltantes(request):
    ordenes_faltantes = OrdenCompra.objects.filter(estado__in=['Faltante'])
    return render(request, 'recepcion/faltantes.html', {'ordenes': ordenes_faltantes})

@login_required
def detalle_faltante(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    faltantes = Faltante.objects.filter(orden=orden).select_related('producto', 'producto__proveedor')

    return render(request, 'recepcion/detalle_faltante.html', {
        'orden': orden,
        'faltantes': faltantes
    })

@login_required
def confirmar_recepcion_faltante(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)

    if request.method == "POST":
        # Obtener faltantes
        faltantes = Faltante.objects.filter(orden=orden)

        # Actualizar stock por cada producto
        for f in faltantes:
            producto = f.producto
            cantidad_a_sumar = f.cantidad_faltante  # Ya viene almacenada
            producto.stock += cantidad_a_sumar
            producto.save()

        # Cambiar estado
        orden.estado = "Recibida"
        orden.save()

        # Eliminar faltantes
        faltantes.delete()

        messages.success(request, f"La orden #{orden.numero} fue marcada como Recibida. El stock ha sido actualizado y los faltantes eliminados.")
        return redirect('faltantes')

    return redirect('detalle_faltante', orden_id=orden_id)

#generar PDF
def generar_pdf_faltante(request, orden_id):
    orden = OrdenCompra.objects.get(numero=orden_id)
    faltantes = Faltante.objects.filter(orden=orden)

    template = get_template("recepcion/pdf_faltante.html")
    html = template.render({"orden": orden, "faltantes": faltantes})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_faltantes_orden_{orden.numero}.pdf"'

    pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response, encoding='UTF-8')

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response