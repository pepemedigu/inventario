from django.shortcuts import render, redirect, get_object_or_404
from .models import Campus,  Edificio, Dependencia, Equipo, ModeloEquipo, Conexion
from datetime import date, datetime
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
import logging
from .forms import EquipoForm

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
def dependencia_view(request, pk, template_name='inventarioav/dependencia/view.html'):
    usuario = request.user
    dependencia = get_object_or_404(Dependencia, pk=pk)
    return render(request, template_name, {'dependencia': dependencia, 'usuario': usuario})

@login_required()
def dependencia_list_equipos(request, pk, tipo_equipo='0' , template_name='inventarioav/dependencia/list_equipos_video.html'):
    usuario = request.user
    dependencia = get_object_or_404(Dependencia, pk=pk)
    if tipo_equipo == '1':
        equipos = dependencia.equipos_video
    elif tipo_equipo == '2':
        equipos = dependencia.equipos_audio
    elif tipo_equipo == '3':
        equipos = dependencia.equipos_control
    elif tipo_equipo == '4':
        equipos = dependencia.equipos_hardware
    elif tipo_equipo == '5':
        equipos = dependencia.equipos_software
    elif tipo_equipo == '6':
        equipos = dependencia.equipos_infraestructura
    else:
        equipos = dependencia.equipos
    return render(request, template_name, {'dependencia': dependencia, 'equipos': equipos, 'usuario': usuario})

@login_required()
def dependencia_create_equipo(request, pk, tipo_equipo='0'):
    usuario = request.user
    dependencia = get_object_or_404(Dependencia, pk=pk)
    print("llego0")
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = Equipo.crear_equipo(dependencia, tipo_equipo, form)
            if equipo is None:
                return render(request, 'inventarioav/error.html',
                              {'error': "No se ha podido crear el equipo", 'usuario': usuario})
        return render(request, 'inventarioav/dependencia/view.html', {'form': form, 'dependencia': dependencia, 'usuario': usuario})
    print("llego")
    form = EquipoForm()
    return render(request, 'inventarioav/dependencia/create_equipo.html', {'form': form, 'dependencia': dependencia, 'tipo_equipo': tipo_equipo, 'usuario': usuario})




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

