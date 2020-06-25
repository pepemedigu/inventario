"""inventario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from inventarioav import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dependencia/view/<int:pk>/', views.dependencia_view, name='dependencia_view'),
    path('dependencia/list_equipos/<int:pk>/<int:tipo_equipo>', views.dependencia_list_equipos, name='dependencia_list_equipos'),
    path('dependencia/create_equipo/<int:pk>/<int:tipo_equipo>', views.dependencia_create_equipo, name='dependencia_create_equipo'),
    path('reports', views.reports, name='reports'),
    path('orders', views.reports, name='orders'),
]