from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ordenes, name='lista_ordenes'),
    path('nueva/', views.crear_orden, name='crear_orden'),
    path('ordenes/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
]