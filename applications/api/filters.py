import django_filters

from applications.establecimientos.models import EstablecimientoProductivo, EstablecimientoNoUniversitario, \
    EstablecimientoUniversitario


def filter_provincia(queryset, name, value):
    lookup = '__'.join([name, 'startswith'])
    return queryset.filter(**{lookup: value})


class EstablecimientoProductivoFilter(django_filters.FilterSet):
    letra = django_filters.CharFilter(field_name='clae2__letra__letra', lookup_expr='exact')
    clae2 = django_filters.CharFilter(field_name='clae2__clae2', lookup_expr='exact')
    provincia_in1 = django_filters.CharFilter(field_name='departamento', method=filter_provincia)

    class Meta:
        model = EstablecimientoProductivo
        fields = ['letra', 'clae2', 'provincia_in1', 'empleo', ]


class EstablecimientoNoUniversitarioFilter(django_filters.FilterSet):
    nivel = django_filters.CharFilter(field_name='titulo__tipo', lookup_expr='exact')
    provincia_in1 = django_filters.CharFilter(field_name='departamento', method=filter_provincia)

    class Meta:
        model = EstablecimientoNoUniversitario
        fields = ['nivel', 'gestion', 'rama', 'area', 'provincia_in1']


class EstablecimientoUniversitarioFilter(django_filters.FilterSet):
    nivel = django_filters.CharFilter(field_name='titulo__tipo', lookup_expr='exact')
    provincia_in1 = django_filters.CharFilter(field_name='departamento', method=filter_provincia)

    class Meta:
        model = EstablecimientoUniversitario
        fields = ['nivel', 'gestion', 'rama', 'area', 'provincia_in1']
