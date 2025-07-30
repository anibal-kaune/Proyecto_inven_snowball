from django.urls import path
from . import views  # Asegúrate de tener un archivo views.py

urlpatterns = [
    path('', views.producto_list, name='producto_list'),
    path('crear/', views.producto_create, name='producto_create'),
    path('<int:pk>/', views.producto_detail, name='producto_detail'),
    path('<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),
    path('marca/', views.marca_list, name='marca_list'),
    path('marca/crear', views.marca_create, name='marca_create'),
    path('marca/<int:pk>/', views.marca_detail, name='marca_detail'),
    path('marca/<int:pk>/editar/', views.marca_update, name='marca_update'),
    path('marca/<int:pk>/eliminar/', views.marca_delete, name='marca_delete'),
]