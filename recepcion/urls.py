from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_recepcion, name='recepcion'),
    path('orden/<int:orden_id>/', views.detalle_orden_recepcion, name='detalle_recepcion'),
    path('orden/<int:orden_id>/confirmar/', views.confirmar_recepcion, name='confirmar_recepcion'),
    path('<int:orden_id>/faltante/', views.reportar_faltante, name='reportar_faltante'),

    path('recibidos/', views.recibidos, name='recibidos'),
    path('recibidos/orden/<int:orden_id>/', views.detalle_recibido, name='detalle_recibido'),
    path('recibidos/orden/<int:orden_id>/pdf/', views.generar_pdf_recibido, name='generar_pdf_recibido'),

    path('faltantes/', views.faltantes, name='faltantes'),
    path('faltantes/orden/<int:orden_id>/', views.detalle_faltante, name='detalle_faltante'),
    path('faltantes/orden/<int:orden_id>/confirmar/', views.confirmar_recepcion_faltante, name='confirmar_recepcion_faltante'),
    path('faltantes/orden/<int:orden_id>/pdf/', views.generar_pdf_faltante, name='generar_pdf_faltante'),
]