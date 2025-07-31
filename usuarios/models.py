from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, rut, email, nombre, apellido, telefono, rol='colaborador', password=None):
        if not email:
            raise ValueError('El email es obligatorio')
        if not rut:
            raise ValueError("El RUT es obligatorio")
        email = self.normalize_email(email)
        usuario = self.model(email=email, rut=rut, nombre=nombre, apellido=apellido, telefono=telefono, rol=rol)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, rut, nombre, apellido, telefono, password):
        usuario = self.create_user(email, rut, nombre, apellido, telefono, password, rol='supervisor')
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = (('colaborador', 'Colaborador'), ('supervisor', 'Supervisor'))
    
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    rol = models.CharField(max_length=15, choices=ROLES, default='colaborador')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['rut', 'nombre', 'apellido', 'telefono']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"
