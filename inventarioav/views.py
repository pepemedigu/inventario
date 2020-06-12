from django.shortcuts import render, redirect, get_object_or_404
from .models import Campus,  Edificio, Dependencia, Equipo, ModeloEquipo, Conexion
from datetime import date, datetime
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
import logging
from .models import Campus,Edificio

logger = logging.getLogger('inventario')
logger_error = logging.getLogger('inventario_error')

campus = Campus.objects.all()
edificios = Edificio.objects.all()
dependencias = Dependencia.objects.all()

@login_required()
def index(request, template_name='inventario/index.html'):
    usuario = request.user
    return render(request, template_name, {'campus': campus, 'edificios': edificios, 'dependencias': dependencias,  'usuario': usuario})

@login_required()
def view(request, pk, template_name='inventario/view.html'):
    usuario = request.user
    dependencia = get_object_or_404(Dependencia, pk=pk)
    equipos = dependencia.equipo_set.all()
    return render(request, template_name, {'dependencia': dependencia, 'equipos': equipos, 'usuario': usuario})

@login_required()
def reports(request, template_name='inventario/reports.html'):
    usuario = request.user
    return render(request, template_name, {'usuario': usuario})

@login_required()
def orders(request, template_name='inventario/orders.html'):
    usuario = request.user
    return render(request, template_name, {'usuario': usuario})
