from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, rut, email, nombre, apellido, telefono, rol='colaborador', password=None):
        if not email:
            raise ValueError('El email es obligatorio')
        user = self.model(
            rut=rut,
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            rol=rol
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, rut, email, nombre, apellido, telefono, password):
        user = self.create_user(rut, email, nombre, apellido, telefono, rol='supervisor', password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

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
        return f"{self.nombre} {self.apellido} ({self.email})"
