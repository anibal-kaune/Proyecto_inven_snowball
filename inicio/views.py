from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from productos.models import Producto
from django.db.models import F
from ordenes.models import OrdenCompra

@login_required
def index(request):
    productos_bajo_minimo = Producto.objects.filter(stock__lt=F('cantidad_minima'))
    ultimas_ordenes = OrdenCompra.objects.select_related('usuario').order_by('-fecha')[:10]  # las 10 más recientes

    return render(request, 'inicio/index.html', {
        'user': request.user,
        'productos_bajo_minimo': productos_bajo_minimo,
        'ultimas_ordenes': ultimas_ordenes,
    })
