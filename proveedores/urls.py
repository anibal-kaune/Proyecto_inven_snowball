from django.urls import path
from . import views  # Asegúrate de tener un archivo views.py

#app_name = 'proveedores'

urlpatterns = [
    path('', views.proveedor_list, name='proveedor_list'),
    path('crear/', views.crear_proveedor, name='crear_proveedor'),
    path('<int:pk>/', views.proveedor_detail, name='proveedor_detail'),
    path('editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
]