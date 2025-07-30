from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    rut_empresa = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=12)

    def __str__(self):
        return self.nombre