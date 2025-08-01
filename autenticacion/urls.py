from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
]
