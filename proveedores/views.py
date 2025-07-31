from django.shortcuts import render, get_object_or_404, redirect
from .models import Proveedor
from .forms import ProveedorForm

def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/proveedor_list.html', {'proveedores': proveedores})

def proveedor_detail(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'proveedores/proveedor_detail.html', {'proveedor': proveedor})

def crear_proveedor(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nombre=request.POST['nombre'],
            rut_empresa=request.POST['rut_empresa'],
            direccion=request.POST['direccion'],
            correo=request.POST['correo'],
            telefono=request.POST['telefono']
        )
        return redirect('proveedor_list')
    return render(request, 'proveedores/proveedor_form.html')

def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.nombre = request.POST['nombre']
        proveedor.rut_empresa = request.POST['rut_empresa']
        proveedor.direccion = request.POST['direccion']
        proveedor.correo = request.POST['correo']
        proveedor.telefono = request.POST['telefono']
        proveedor.save()
        return redirect('proveedor_list')
    return render(request, 'proveedores/proveedor_editar.html', {'proveedor': proveedor})

def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor_list')
    return render(request, 'proveedores/proveedor_delete.html', {'proveedor': proveedor})
