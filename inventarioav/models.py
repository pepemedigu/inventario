from django.db import models
import logging
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime, timedelta
from django.utils import timezone
import requests
from urllib.parse import quote
import xml.etree.ElementTree as ET
from django.conf import settings
import re

logger = logging.getLogger('inventario')
logger_error = logging.getLogger('inventario_error')

class Campus(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100, unique=True)
    order = models.IntegerField(unique=True, null=False)

    class Meta:
        verbose_name_plural = "Campus"
        ordering = ["order"]

    def __str__(self):
        return self.nombre

class Edificio(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.DO_NOTHING, null=False)

    class Meta:
        ordering = ["campus", "nombre"]

    def __str__(self):
        return self.nombre

class TipoDependencia(models.IntegerChoices):
    AULA = 1, _('Aula de Docencia')
    AULA_SEMIPRESENCIAL = 2, _('Aula de Docencia Semipresencial')
    SALA_REUNIONES = 3, _('Sala de Reuniones')
    SALA_REUNIONES_VIDEOCONFERENCIA = 4, _('Sala de Reuniones Por Videoconferencia')
    SALA_TELEPRESENCIA = 5, _('Sala de Telepresencia')
    SALA_TELEDOCENCIA_DIRECTO = 6, _('Sala de Teledocencia en Directo')
    ESTUDIO_GRABACION_TELEDOCENCIA = 7, _('Estudio de Grabación de Teledocencia')
    AULA_GRADOS = 8, _('Aula de Grados')
    SALON_ACTOS = 9, _('Salón de Actos')
    DESPACHO = 10, _('Despacho')

class Dependencia(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100, unique=True)
    edificio = models.ForeignKey(Edificio, on_delete=models.DO_NOTHING, null=False)
    tipo = models.IntegerField(choices=TipoDependencia.choices)

    class Meta:
        ordering = ["edificio", "nombre"]

    def __str__(self):
        return self.nombre

    def equipos(self):
        return self.equipos.all()
    def equipos_video(self):
        return self.equipo_set.filter(tipo="1")
    def equipos_audio(self):
        return self.equipo_set.filter(tipo="2")
    def equipos_control(self):
        return self.equipo_set.filter(tipo="3")
    def equipos_hardware(self):
        return self.equipo_set.filter(tipo="4")
    def equipos_software(self):
        return self.equipo_set.filter(tipo="5")
    def equipos_infraestructura(self):
        return self.equipo_set.filter(tipo="6")

class TipoEquipo(models.IntegerChoices):
    VIDEO = 1, _('Vídeo')
    AUDIO = 2, _('Audio')
    CONTROL = 3, _('Control')
    HARDWARE = 4, _('Hardware')
    SOFTWARE = 5, _('Software')
    INFRAESTRUCTURA= 6, _('Infraestructura')

class ModeloEquipo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100, unique=True, null=True)
    tipo = models.IntegerField(choices=TipoEquipo.choices)

    class Meta:
        verbose_name = "Modelo de equipo"
        verbose_name_plural = "Modelos de equipo"
        ordering = ["tipo","nombre"]

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.IntegerField(choices=TipoEquipo.choices)
    modelo = models.ForeignKey(ModeloEquipo, on_delete=models.SET_NULL, null=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True)
    conexiones = models.ManyToManyField(
        'self',
        through="Conexion",
        through_fields=('equipo_origen', 'equipo_destino'),
    )

    class Meta:
        ordering = ["tipo", "nombre"]

    def __str__(self):
        return self.nombre


class TipoConexion(models.IntegerChoices):
    UTP = 1, _('Cable UTP')
    HDMI = 2, _('Cable HDMI')
    AUDIO = 3, _('Cable de audio')
    FIBRA = 4, _('Cable de fibra óptica')

class Conexion(models.Model):
    equipo_origen = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=False)
    equipo_destino = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=False, related_name="conexion_destino")
    puerto_origen = models.CharField(max_length=50,  null=True)
    puerto_destino = models.CharField(max_length=50, null=True)
    tipo = models.IntegerField(choices=TipoConexion.choices, null=False)
    comentario = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "Conexión"
        verbose_name_plural = "Conexiones"
        ordering = ["equipo_origen", "equipo_destino"]

    def __str__(self):
        return f"{self.equipo_origen.nombre} ->  {self.equipo_origen.nombre} | {self.tipo}"




