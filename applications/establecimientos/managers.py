from django.db import models
from django.db.models import Value, CharField, F


class TipoTituloManager(models.Manager):
    def get_distinct_descriptions_grouped(self):
        from applications.establecimientos.models import EstablecimientoUniversitario, EstablecimientoNoUniversitario

        universitarios = EstablecimientoUniversitario.objects.annotate(
            id_tipo_titulo=F('tipo_titulo_id'),
            descripcion_tipo_titulo=F('tipo_titulo__descripcion')
        ).values('id_tipo_titulo', 'descripcion_tipo_titulo')

        no_universitarios = EstablecimientoNoUniversitario.objects.annotate(
            id_tipo_titulo=F('titulo__tipo_id'),
            descripcion_tipo_titulo=F('titulo__tipo__descripcion')
        ).values('id_tipo_titulo', 'descripcion_tipo_titulo')

        universitarios = universitarios.annotate(tipo_establecimiento=Value('universitarios', output_field=CharField()))
        no_universitarios = no_universitarios.annotate(
            tipo_establecimiento=Value('no_universitarios', output_field=CharField()))

        queryset = universitarios.union(no_universitarios).order_by("id_tipo_titulo")

        return queryset
