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
def index(request, template_name='inventarioav/index.html'):
    usuario = request.user
    return render(request, template_name, {'campus': campus,  'usuario': usuario})

@login_required()
def view(request, pk, template_name='inventarioav/view.html'):
    usuario = request.user
    dependencia = get_object_or_404(Dependencia, pk=pk)
    equipos = dependencia.equipo_set.all()
    return render(request, template_name, {'dependencia': dependencia, 'equipos': equipos, 'usuario': usuario})

@login_required()
def reports(request, template_name='inventarioav/reports.html'):
    usuario = request.user
    reports = []
    return render(request, template_name, {'reports': reports,'usuario': usuario})

@login_required()
def orders(request, template_name='inventarioav/orders.html'):
    usuario = request.user
    orders = []
    return render(request, template_name, {'orders': orders,'usuario': usuario})
