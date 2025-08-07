from django.urls import path

from .views import (UniversidadImportView, FacultadImportView, EstablecimientoUniversitarioImportView, RamaImportView,
                    TituloImportView,
                    AreaDeEstudioImportView, EstablecimientoNoUniversitarioImportView,
                    EstablecimientoProductivoImportView, LetraImportView, DimensionEmpresaImportView,
                    CLAE2ImportView, GestionImportView, TipoTituloImportView, EscuelaImportView, UnidadMedidaImportView,
                    EstudioUniversitarioImportView, EstudioNoUniversitarioImportView)

app_name = "establecimientos"

urlpatterns = [
    path('importar-universidad/', UniversidadImportView.as_view(), name='importar-universidad'),
    path('importar-facultad/', FacultadImportView.as_view(), name='importar-facultad'),
    path('importar-establecimiento-universitario/', EstablecimientoUniversitarioImportView.as_view(),
         name='importar-establecimiento-universitario'),
    path('importar-escuela/', EscuelaImportView.as_view(), name='importar-escuela'),
    path('importar-establecimiento-no-universitario/', EstablecimientoNoUniversitarioImportView.as_view(),
         name='importar-establecimiento-no-universitario'),
    path('importar-establecimiento-productivo/', EstablecimientoProductivoImportView.as_view(),
         name='importar-establecimiento-productivo'),
    path('importar-tipo-titulo/', TipoTituloImportView.as_view(), name='importar-tipo-titulo'),
    path('importar-titulo/', TituloImportView.as_view(), name='importar-titulo'),
    path('importar-gestion/', GestionImportView.as_view(), name='importar-gestion'),
    path('importar-unidad-medida/', UnidadMedidaImportView.as_view(), name='importar-unidad-medida'),
    path('importar-area-de-estudio/', AreaDeEstudioImportView.as_view(), name='importar-area-de-estudio'),
    path('importar-rama/', RamaImportView.as_view(), name='importar-rama'),
    path('importar-letra/', LetraImportView.as_view(), name='importar-letra'),
    path('importar-estudio-universitario/', EstudioUniversitarioImportView.as_view(),
         name='importar-estudios-universitarios'),
    path('importar-estudio-no-universitario/', EstudioNoUniversitarioImportView.as_view(),
         name='importar-estudios-no-universitarios'),
    path('importar-clae2/', CLAE2ImportView.as_view(), name='importar-clae2'),
    path('importar-dimension-empresa/', DimensionEmpresaImportView.as_view(), name='importar-dimension-empresa'),
]
