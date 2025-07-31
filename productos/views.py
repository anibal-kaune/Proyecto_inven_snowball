from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Marca
from proveedores.models import Proveedor
from .forms import ProductoForm, MarcaForm

#Vistas producto
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'productos/producto_list.html', {'productos': productos})

def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_detail.html', {'producto': producto})

"""def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/producto_form.html', {'form': form})"""

def producto_create(request):
    proveedores = Proveedor.objects.all()
    if request.method == 'POST':
        Producto.objects.create(
            codigo=request.POST['codigo'],
            nombre=request.POST['nombre'],
            precio_venta=request.POST['precio_venta'],
            precio_compra=request.POST['precio_compra'],
            descripcion=request.POST['descripcion'],
            cantidad_minima=request.POST['cantidad_minima'],
            stock=request.POST['stock'],
            marca=request.POST['marca'],
            proveedor_id=request.POST['proveedor']
        )
        return redirect('producto_list')
    return render(request, 'productos/producto_form.html', {'proveedores': proveedores})

def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto_detail', pk=pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/producto_form.html', {'form': form})

def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('producto_list')
    return render(request, 'productos/producto_delete.html', {'producto': producto})



def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/producto_list.html', {'productos': productos})


def crear_producto(request):
    proveedores = Proveedor.objects.all()
    if request.method == 'POST':
        Producto.objects.create(
            codigo=request.POST['codigo'],
            nombre=request.POST['nombre'],
            precio_venta=request.POST['precio_venta'],
            precio_compra=request.POST['precio_compra'],
            descripcion=request.POST['descripcion'],
            cantidad_minima=request.POST['cantidad_minima'],
            stock=request.POST['stock'],
            marca=request.POST['marca'],
            proveedor_id=request.POST['proveedor']
        )
        return redirect('listar_productos')
    return render(request, 'productos/producto_form.html', {'proveedores': proveedores})


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    proveedores = Proveedor.objects.all()
    if request.method == 'POST':
        producto.codigo = request.POST['codigo']
        producto.nombre = request.POST['nombre']
        producto.precio_venta = request.POST['precio_venta']
        producto.precio_compra = request.POST['precio_compra']
        producto.descripcion = request.POST['descripcion']
        producto.cantidad_minima = request.POST['cantidad_minima']
        producto.stock = request.POST['stock']
        producto.marca = request.POST['marca']
        producto.proveedor_id = request.POST['proveedor']
        producto.save()
        return redirect('listar_productos')
    return render(request, 'productos/producto_editar.html', {'producto': producto, 'proveedores': proveedores})


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'productos/producto_delete.html', {'producto': producto})

#vistas marca
def marca_list(request):
    marca = Marca.objects.all()
    return render(request, 'productos/marca_list.html', {'marca': marca})

def marca_detail(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    return render(request, 'productos/marca_detail.html', {'marca': marca})

def crear_marca(request):
    proveedores = Proveedor.objects.all()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        proveedor_id = request.POST.get('proveedor')
        proveedor = Proveedor.objects.get(id=proveedor_id) if proveedor_id else None
        Marca.objects.create(nombre=nombre, proveedor=proveedor)
        return redirect('listar_marcas')
    return render(request, 'productos/marca_form.html', {'proveedores': proveedores})


def editar_marca(request, id):
    marca = get_object_or_404(Marca, id=id)
    proveedores = Proveedor.objects.all()
    if request.method == 'POST':
        marca.nombre = request.POST['nombre']
        proveedor_id = request.POST.get('proveedor')
        marca.proveedor = Proveedor.objects.get(id=proveedor_id) if proveedor_id else None
        marca.save()
        return redirect('listar_marcas')
    return render(request, 'productos/marca_editar.html', {'marca': marca, 'proveedores': proveedores})
def eliminar_marca(request, id):
    marca = get_object_or_404(Marca, id=id)
    if request.method == 'POST':
        marca.delete()
        return redirect('listar_marcas')
    return render(request, 'productos/marca_delete.html', {'marca': marca})