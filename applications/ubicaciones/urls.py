from django.urls import path

from applications.ubicaciones.views import SectorMayoritarioImportView, TasaEmpleoFormalImportView

app_name = 'ubicaciones'

urlpatterns = [
    path('importar-sectores-mayoritarios/', SectorMayoritarioImportView.as_view(),
         name='importar-sectores-mayoritarios'),
    path('importar-tasa-empleo-formal/', TasaEmpleoFormalImportView.as_view(),
         name='importar-tasa-empleo-formal'),
]
