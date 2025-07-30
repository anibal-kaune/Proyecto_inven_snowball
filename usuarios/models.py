from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, rut, nombre, apellido, telefono, email, password=None, rol='colaborador'):
        if not rut:
            raise ValueError('El usuario debe tener RUT')
        if not email:
            raise ValueError('El usuario debe tener email')

        email = self.normalize_email(email)
        user = self.model(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            rol=rol
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rut, nombre, apellido, telefono, email, password):
        user = self.create_user(rut, nombre, apellido, telefono, email, password, rol='supervisor')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    ROL_CHOICES = [
        ('supervisor', 'Supervisor'),
        ('colaborador', 'Colaborador'),
    ]

    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='colaborador')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['rut', 'nombre', 'apellido', 'telefono']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"
