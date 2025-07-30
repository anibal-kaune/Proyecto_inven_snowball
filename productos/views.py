from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, Marca
from .forms import ProductoForm, MarcaForm

#Vistas producto
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'productos/producto_list.html', {'productos': productos})

def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_detail.html', {'producto': producto})

def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'productos/producto_form.html', {'form': form})

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

#vistas marca
def marca_list(request):
    marca = Marca.objects.all()
    return render(request, 'productos/marca_list.html', {'marca': marca})

def marca_detail(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    return render(request, 'productos/marca_detail.html', {'marca': marca})

def marca_create(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marca_list')
    else:
        form = MarcaForm()
    return render(request, 'productos/marca_form.html', {'form': form})

def marca_update(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        form = MarcaForm(request.POST, request.FILES, instance=marca)
        if form.is_valid():
            form.save()
            return redirect('marca_detail', pk=pk)
    else:
        form = MarcaForm(instance=marca)
    return render(request, 'productos/marca_form.html', {'form': form})

def marca_delete(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        marca.delete()
        return redirect('marca_list')
    return render(request, 'productos/marca_delete.html', {'marca': marca})
