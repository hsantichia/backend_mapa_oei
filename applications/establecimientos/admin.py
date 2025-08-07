from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import *


class EstablecimientoUniversitarioAdmin(GISModelAdmin):
    list_display = ["facultad", "universidad", "titulo", "rama", "area"]


class EstablecimientoNoUniversitarioAdmin(GISModelAdmin):
    list_display = ["escuela", "gestion", "titulo", "area"]


class EstablecimientoProductivoAdmin(GISModelAdmin):
    list_display = ["clae2", "empleo"]


class UnidadMedidaAdmin(GISModelAdmin):
    list_display = ["id", "descripcion"]
    list_display_links = ["descripcion"]


class LetraAdmin(admin.ModelAdmin):
    list_display = ["letra", "letra_desc"]
    list_display_links = ["letra_desc"]


class CLAE2Admin(admin.ModelAdmin):
    list_display = ["clae2", "clae2_desc"]
    list_display_links = ["clae2_desc"]


class TituloAdmin(admin.ModelAdmin):
    list_display = ["tipo", "nombre"]
    list_display_links = ["nombre"]


admin.site.register(Universidad)
admin.site.register(Facultad)
admin.site.register(EstablecimientoUniversitario, EstablecimientoUniversitarioAdmin)
admin.site.register(Escuela)
admin.site.register(EstablecimientoNoUniversitario, EstablecimientoNoUniversitarioAdmin)
admin.site.register(EstablecimientoProductivo, EstablecimientoProductivoAdmin)
admin.site.register(DimensionEmpresa)
admin.site.register(Gestion)
admin.site.register(UnidadMedida, UnidadMedidaAdmin)
admin.site.register(Letra, LetraAdmin)
admin.site.register(CLAE2, CLAE2Admin)
admin.site.register(Rama)
admin.site.register(AreaDeEstudio)
admin.site.register(TipoTitulo)
admin.site.register(Titulo, TituloAdmin)
