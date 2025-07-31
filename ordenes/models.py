from django.db import models
from django.utils import timezone
from usuarios.models import Usuario
from productos.models import Producto

class OrdenCompra(models.Model):
    ESTADOS = [
        ('Emitida', 'Emitida'),
        ('Aprobada', 'Aprobada'),
        ('Cancelada', 'Cancelada'),
        ('Recibida', 'Recibida'),
    ]

    numero = models.AutoField(primary_key=True)
    fecha = models.DateField(default=timezone.now)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Emitida')

    def total_general(self):
        return sum(item.total_producto() for item in self.items.all())

    def __str__(self):
        return f'Orden #{self.numero} - {self.estado}'


class ItemOrdenCompra(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()

    class Meta:
        unique_together = ('orden', 'producto')  # Evita productos duplicados en una orden

    def precio_unitario(self):
        return self.producto.precio_compra

    def total_producto(self):
        return self.cantidad * self.precio_unitario()

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'