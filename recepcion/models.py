from django.db import models
from django.utils import timezone
from ordenes.models import OrdenCompra, Producto
from usuarios.models import Usuario

class Faltante(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_solicitada = models.PositiveIntegerField()
    cantidad_recibida = models.PositiveIntegerField()
    cantidad_faltante = models.PositiveIntegerField()
    fecha_reporte = models.DateTimeField(default=timezone.now)
    reportado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.cantidad_faltante = max(self.cantidad_solicitada - self.cantidad_recibida, 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Faltante en Orden #{self.orden.numero} - {self.producto.nombre}'