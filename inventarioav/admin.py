from django.contrib import admin
from .models import Campus, Edificio, Dependencia, Equipo, ModeloEquipo, Conexion

admin.site.register(Campus)
admin.site.register(Edificio)
admin.site.register(Dependencia)
admin.site.register(Equipo)
admin.site.register(ModeloEquipo)
admin.site.register(Conexion)
