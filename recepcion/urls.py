from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_recepcion, name='recepcion'),
    path('orden/<int:orden_id>/', views.detalle_orden_recepcion, name='detalle_recepcion'),
    path('orden/<int:orden_id>/confirmar/', views.confirmar_recepcion, name='confirmar_recepcion'),
    path('<int:orden_id>/faltante/', views.reportar_faltante, name='reportar_faltante'),

    path('recibidos/', views.recibidos, name='recibidos'),
]