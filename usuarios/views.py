from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.contrib import messages

# solo los supervisores pueden acceder
def es_supervisor(user):
    return user.is_authenticated and user.rol == 'supervisor'

@login_required
def listar_usuarios(request):
    if not es_supervisor(request.user):
        return redirect('index')
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar.html', {'usuarios': usuarios})

@login_required
def crear_usuario(request):
    if not es_supervisor(request.user):
        return redirect('index')
    if request.method == 'POST':
        rut = request.POST['rut']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        telefono = request.POST['telefono']
        rol = request.POST.get('rol', 'colaborador')
        password = request.POST['password']

        if Usuario.objects.filter(rut=rut).exists():
            messages.error(request, 'El RUT ya está registrado.')
            return redirect('crear_usuario')
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return redirect('crear_usuario')

        Usuario.objects.create_user(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            password=password,
            rol=rol
        )
        return redirect('listar_usuarios')

    return render(request, 'usuarios/crear.html')

@login_required
def editar_usuario(request, id):
    if not es_supervisor(request.user):
        return redirect('index')
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.nombre = request.POST['nombre']
        usuario.apellido = request.POST['apellido']
        usuario.telefono = request.POST['telefono']
        usuario.rol = request.POST.get('rol', 'colaborador')
        usuario.save()
        return redirect('listar_usuarios')
    return render(request, 'usuarios/editar.html', {'usuario': usuario})

@login_required
def eliminar_usuario(request, id):
    if not es_supervisor(request.user):
        return redirect('index')
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})
