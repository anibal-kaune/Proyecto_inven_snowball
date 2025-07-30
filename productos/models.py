from django.db import models
from proveedores.models import Proveedor

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    proveedor = models.ForeignKey(Proveedor,null=True,blank=True,on_delete=models.SET_NULL,related_name='marcas')

    def proveedor_nombre(self):
        return self.proveedor.nombre if self.proveedor else "sin proveedor"

    def __str__(self):
        return f"{self.nombre} - {self.proveedor_nombre()}"

class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    #imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    descripcion = models.TextField(blank=True)
    cantidad_minima = models.PositiveIntegerField()
    stock = models.IntegerField(default=0)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
