from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers
from rest_framework.authtoken import views

from .views import EstablecimientoUniversitarioList, EstablecimientoNoUniversitarioList, \
    EstablecimientoProductivoList, CLAE2List, ProvinciaGeoJSONList, DepartamentoGeoJSONList, LetraList, \
    EstudioUniversitarioList, EstudioNoUniversitarioList, TipoGestionList, EmpleoList, TipoTituloList

router = routers.DefaultRouter()

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="API proyecto georreferenciación",
        default_version='v1',
        description="Georreferenciamiento de establecimientos educativos, \
            tanto universitarios como no universitarios, y establecimientos productivos",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('', include(router.urls)),
    path('provincias-geojson/', ProvinciaGeoJSONList.as_view(),
         name='provincias-geojson'),
    path('departamentos-geojson/', DepartamentoGeoJSONList.as_view(),
         name='departamentos-geojson'),
    path('establecimientos-universitarios/', EstablecimientoUniversitarioList.as_view(),
         name='establecimientos-universitarios-list'),
    path('establecimientos-no-universitarios/', EstablecimientoNoUniversitarioList.as_view(),
         name='establecimientos-no-universitarios-list'),
    path('establecimientos-productivos/', EstablecimientoProductivoList.as_view(),
         name='establecimientos-productivo-list'),
    path('letra/', LetraList.as_view(), name='letra-list'),
    path('clae2/', CLAE2List.as_view(), name='clae2-list'),
    path('estudio-universitario/', EstudioUniversitarioList.as_view(), name='estudio-universitario-list'),
    path('estudio-no-universitario/', EstudioNoUniversitarioList.as_view(), name='estudio-no-universitario-list'),
    path('tipo-gestion/', TipoGestionList.as_view(), name='tipo-gestion-list'),
    path('empleo/', EmpleoList.as_view(), name='empleo-list'),
    path('tipo-titulo/', TipoTituloList.as_view(), name='tipo-titulo-list'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token-auth/', views.obtain_auth_token),
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-doc'),
]
