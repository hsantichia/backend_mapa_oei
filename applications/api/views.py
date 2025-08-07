from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from applications.api.filters import EstablecimientoProductivoFilter, EstablecimientoNoUniversitarioFilter, \
    EstablecimientoUniversitarioFilter
from applications.api.serializers import EstablecimientoUniversitarioSerializer, \
    EstablecimientoNoUniversitarioSerializer, EstablecimientoProductivoSerializer, CLAE2Serializer, ProvinciaSerializer, \
    DepartamentoSerializer, LetraSerializer, EstudioUniversitarioSerializer, EstudioNoUniversitarioSerializer, \
    TipoGestionSerializer, EmpleoSerializer, TipoTituloSerializer
from applications.establecimientos.models import EstablecimientoUniversitario, EstablecimientoNoUniversitario, \
    EstablecimientoProductivo, Letra, CLAE2, EstudioUniversitario, EstudioNoUniversitario, Gestion, DimensionEmpresa, \
    TipoTitulo
from applications.ubicaciones.models import Provincia, Departamento


class EstablecimientoUniversitarioList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EstablecimientoUniversitario.objects.all().distinct("facultad")
    serializer_class = EstablecimientoUniversitarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstablecimientoUniversitarioFilter


class EstablecimientoNoUniversitarioList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EstablecimientoNoUniversitario.objects.all().distinct("escuela")
    serializer_class = EstablecimientoNoUniversitarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstablecimientoNoUniversitarioFilter


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class EstablecimientoProductivoList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EstablecimientoProductivo.objects.all().order_by("clae2")
    serializer_class = EstablecimientoProductivoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstablecimientoProductivoFilter


class LetraList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Letra.objects.all().order_by("letra")
    serializer_class = LetraSerializer


class CLAE2List(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CLAE2.objects.all().order_by("clae2")
    serializer_class = CLAE2Serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['letra__letra', ]


class EstudioUniversitarioList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EstudioUniversitario.objects.all().order_by("rama")
    serializer_class = EstudioUniversitarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rama__id', ]


class EstudioNoUniversitarioList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EstudioNoUniversitario.objects.all().order_by("area_id")
    serializer_class = EstudioNoUniversitarioSerializer
    filter_backends = [DjangoFilterBackend]


class TipoTituloList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TipoTitulo.objects.get_distinct_descriptions_grouped()
    serializer_class = TipoTituloSerializer
    filter_backends = [DjangoFilterBackend]


class TipoGestionList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Gestion.objects.all().order_by("id")
    serializer_class = TipoGestionSerializer
    filter_backends = [DjangoFilterBackend]


class EmpleoList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DimensionEmpresa.objects.all().order_by("id")
    serializer_class = EmpleoSerializer
    filter_backends = [DjangoFilterBackend]


class ProvinciaGeoJSONList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Provincia.objects.all().order_by("in1")
    serializer_class = ProvinciaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['in1', ]


class DepartamentoGeoJSONList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Departamento.objects.all().order_by("in1")
    serializer_class = DepartamentoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['provincia_in1', ]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
