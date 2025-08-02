from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistroUsuarioForm, LoginForm
from usuarios.models import Usuario
from productos.models import Producto
from django.db.models import F
from ordenes.models import OrdenCompra

def es_supervisor(user):
    return user.rol == 'supervisor'

@user_passes_test(es_supervisor)
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    productos_bajo_minimo = Producto.objects.filter(stock__lt=F('cantidad_minima'))
    ultimas_ordenes = OrdenCompra.objects.select_related('usuario').order_by('-fecha')[:10]  # las 10 más recientes

    return render(request, 'inicio/index.html', {
        'user': request.user,
        'productos_bajo_minimo': productos_bajo_minimo,
        'ultimas_ordenes': ultimas_ordenes,
    })
