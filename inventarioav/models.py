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
    codigo = models.CharField("Código del campus", max_length=50, unique=True)
    nombre = models.CharField("Nombre", max_length=100, unique=True)
    order = models.IntegerField("Orden", unique=True, null=False)

    class Meta:
        verbose_name_plural = "Campus"
        ordering = ["order"]

    def __str__(self):
        return self.nombre

class Edificio(models.Model):
    codigo = models.CharField("Código de edificio", max_length=50, unique=True)
    nombre = models.CharField("Nombre", max_length=100, unique=True)
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
    codigo = models.CharField("Código de dependencia", max_length=50, unique=True)
    nombre = models.CharField("Nombre de la dependencia", max_length=100, unique=True)
    edificio = models.ForeignKey(Edificio, on_delete=models.DO_NOTHING, null=False)
    tipo = models.IntegerField("Tipo de dependencia", choices=TipoDependencia.choices)

    class Meta:
        ordering = ["edificio", "nombre"]

    def __str__(self):
        return self.nombre

    @property
    def equipos(self):
        return self.equipos.all()

    @property
    def equipos_video(self):
        return self.equipo_set.filter(tipo="1")

    @property
    def equipos_audio(self):
        return self.equipo_set.filter(tipo="2")

    @property
    def equipos_control(self):
        return self.equipo_set.filter(tipo="3")

    @property
    def equipos_hardware(self):
        return self.equipo_set.filter(tipo="4")

    @property
    def equipos_software(self):
        return self.equipo_set.filter(tipo="5")

    @property
    def equipos_infraestructura(self):
        return self.equipo_set.filter(tipo="6")

class TipoEquipo(models.IntegerChoices):
    VIDEO = 1, _('Vídeo')
    AUDIO = 2, _('Audio')
    CONTROL = 3, _('Control')
    HARDWARE = 4, _('Hardware')
    SOFTWARE = 5, _('Software')
    INFRAESTRUCTURA= 6, _('Infraestructura')

    @property
    def nombre(self):
        return self.label

    def __str__(self):
        return self.label

class ModeloEquipo(models.Model):
    codigo = models.CharField("Código de modelo", max_length=50, unique=True)
    nombre = models.CharField("Nombre de modelo",  max_length=100, unique=True, null=True)
    tipo = models.IntegerField("Tipo de modelo", choices=TipoEquipo.choices)

    class Meta:
        verbose_name = "Modelo de equipo"
        verbose_name_plural = "Modelos de equipo"
        ordering = ["tipo","nombre"]

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    nombre = models.CharField("Nombre", max_length=100, null=True, editable=False)
    tipo = models.IntegerField("Tipo de equipo", choices=TipoEquipo.choices, null=True, editable=False)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_DEFAULT, default=None, null=False, editable=False)
    modelo = models.ForeignKey(ModeloEquipo, on_delete=models.SET_DEFAULT,  default=None, null=False)
    numero_serie = models.CharField("Número de serie", max_length=50, default=1, null=False)
    numero_inventario = models.CharField("Número de inventario", max_length=50, null=True)
    codigo_suministro = models.CharField("Código de suministro", max_length=50, null=True)
    fecha_suministro = models.DateField("Fecha de suministro", null=True)
    fecha_instalacion = models.DateField("Fecha de instalación",  null=True)
    fecha_fin_garantia = models.DateField("Fecha fin de Garantía", null=True)
    comentarios = models.TextField("Comentarios", max_length=400, null=True)
    conexiones = models.ManyToManyField(
        'self',
        through="Conexion",
        through_fields=('equipo_origen', 'equipo_destino'),
    )

    class Meta:
        ordering = ["tipo", "nombre"]

    def __str__(self):
        return self.nombre

    @property
    def conexiones_origen(self):
        return Conexion.objects.filter(equipo_origen__id=self.id)

    @property
    def conexiones_destino(self):
        return Conexion.objects.filter(equipo_destino__id=self.id)

    @property
    def tipo_nombre(self):
        return TipoEquipo(self.tipo).label

    def crear_equipo(dependencia, tipo_equipo, form):
        equipo = Equipo(modelo=form.cleaned_data['modelo'], numero_serie=form.cleaned_data['numero_serie'], numero_inventario=form.cleaned_data['numero_inventario'],
               codigo_suministro=form.cleaned_data['codigo_suministro'],
               fecha_suministro=form.cleaned_data['fecha_suministro'],
               fecha_instalacion=form.cleaned_data['fecha_instalacion'], fecha_fin_garantia=form.cleaned_data['fecha_fin_garantia'], comentarios=form.cleaned_data['comentarios'])
        equipo.dependencia = dependencia
        equipo.tipo = tipo_equipo if tipo_equipo in TipoEquipo.values else '1' #Ojo si el tipo no es válido guarda 1 (Vídeo)
        equipo.nombre = f"{equipo.modelo}-{equipo.numero_serie}"
        equipo.save()
        return equipo


class TipoConexion(models.IntegerChoices):
    UTP = 1, _('Cable UTP')
    HDMI = 2, _('Cable HDMI')
    AUDIO = 3, _('Cable de audio')
    FIBRA = 4, _('Cable de fibra óptica')

class Conexion(models.Model):
    equipo_origen = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=False, related_name="equipo_origen")
    equipo_destino = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=False, related_name="equipo_destino")
    puerto_origen = models.CharField("Puerto equipo de origen", max_length=50,  null=True)
    puerto_destino = models.CharField("Puerto equipo de destino", max_length=50, null=True)
    tipo = models.IntegerField("Tipo de conexión", choices=TipoConexion.choices, null=False)
    comentario = models.CharField("Comentario", max_length=100, null=True)

    class Meta:
        verbose_name = "Conexión"
        verbose_name_plural = "Conexiones"
        ordering = ["equipo_origen", "equipo_destino"]

    def __str__(self):
        return f"{self.equipo_origen.nombre} ->  {self.equipo_destino.nombre} | {TipoConexion(self.tipo).label}"

    def tipo_nombre(self):
        return TipoConexion(self.tipo).label


