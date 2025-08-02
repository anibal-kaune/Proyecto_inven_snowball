from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from productos.models import Producto
from django.db.models import F

@login_required
def index(request):
    productos_bajo_minimo = Producto.objects.filter(stock__lt=F('cantidad_minima'))
    return render(request, 'index.html', {
        'user': request.user,
        'productos_bajo_minimo': productos_bajo_minimo,
    })