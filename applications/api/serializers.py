from django.db.models import Count
from django.db.models.functions import Substr
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from applications.establecimientos.models import EstablecimientoUniversitario, EstablecimientoNoUniversitario, \
    EstablecimientoProductivo, CLAE2, Letra, EstudioUniversitario, EstudioNoUniversitario, Gestion, DimensionEmpresa
from applications.ubicaciones.models import Provincia, Departamento, SectorMayoritario, TasaEmpleoFormal


class TituloSerializer(serializers.Serializer):
    nombre = serializers.CharField(source="titulo.nombre", read_only=True)
    rama = serializers.CharField(source="rama.nombre", read_only=True)
    area = serializers.CharField(source="area.descripcion", read_only=True)
    duracion = serializers.IntegerField(read_only=True)
    unidad_medida = serializers.CharField(source="unidad_medida.descripcion", read_only=True)


class EstablecimientoUniversitarioSerializer(GeoFeatureModelSerializer):
    universidad = serializers.CharField(source="universidad.nombre", read_only=True)
    facultad = serializers.CharField(source="facultad.nombre", read_only=True)
    gestion = serializers.CharField(source="gestion.descripcion", read_only=True)
    nivel = serializers.CharField(source="titulo.tipo.descripcion", read_only=True)
    titulos = serializers.SerializerMethodField()
    nam_departamento = serializers.SerializerMethodField()
    nam_provincia = serializers.SerializerMethodField()

    class Meta:
        model = EstablecimientoUniversitario
        geo_field = "lat_lon"
        fields = (
            "universidad",
            "facultad",
            "gestion",
            "nivel",
            "titulos",
            "nam_departamento",
            "nam_provincia",
        )

    @staticmethod
    def get_titulos(instance):
        facultad = EstablecimientoUniversitario.objects.filter(facultad=instance.facultad, rama=instance.rama,
                                                               area=instance.area)
        titulos = TituloSerializer(facultad, many=True).data
        return titulos

    @staticmethod
    def get_nam_departamento(instance):
        departamento = Departamento.objects.filter(in1=instance.departamento)
        return instance.departamento if departamento.exists() else departamento.first().nam

    @staticmethod
    def get_nam_provincia(instance):
        departamento = Departamento.objects.filter(in1=instance.departamento)
        return instance.departamento[:2] if departamento.exists() else departamento.first().provincia_in1.nam


class EstablecimientoNoUniversitarioSerializer(GeoFeatureModelSerializer):
    nombre = serializers.CharField(source="escuela.nombre", read_only=True)
    gestion = serializers.CharField(source="gestion.descripcion", read_only=True)
    nivel = serializers.CharField(source="titulo.tipo.descripcion", read_only=True)
    titulos = serializers.SerializerMethodField()
    nam_departamento = serializers.SerializerMethodField()
    nam_provincia = serializers.SerializerMethodField()

    class Meta:
        model = EstablecimientoNoUniversitario
        geo_field = "lat_lon"
        fields = ("nombre", "titulo", "gestion", "nivel", "titulos", "nam_departamento", "nam_provincia")

    @staticmethod
    def get_titulos(instance):
        establecimiento = EstablecimientoNoUniversitario.objects.filter(escuela=instance.escuela, rama=instance.rama,
                                                                        area=instance.area)
        titulos = TituloSerializer(establecimiento, many=True).data
        return titulos

    @staticmethod
    def get_nam_departamento(instance):
        departamento = Departamento.objects.filter(in1=instance.departamento)
        if departamento.exists():
            return departamento.first().nam
        return instance.departamento

    @staticmethod
    def get_nam_provincia(instance):
        departamento = Departamento.objects.filter(in1=instance.departamento)
        if departamento.exists():
            return departamento.first().provincia_in1.nam
        return instance.departamento[:2]


class EstablecimientoProductivoSerializer(GeoFeatureModelSerializer):
    empleo = serializers.CharField(source="empleo.descripcion", read_only=True)
    letra = serializers.CharField(source="clae2.letra", read_only=True)
    clae2 = serializers.CharField(source="clae2.clae2_desc", read_only=True)
    nam_departamento = serializers.SerializerMethodField()
    nam_provincia = serializers.SerializerMethodField()

    class Meta:
        model = EstablecimientoProductivo
        geo_field = "lat_lon"
        fields = ("empleo", "letra", "clae2", "proporcion_mujeres", "nam_departamento", "nam_provincia")
        auto_bbox = True

    @staticmethod
    def get_nam_departamento(instance):
        departamento = Departamento.objects.filter(in1=instance.departamento)
        if departamento.exists():
            return departamento.first().nam
        return instance.departamento

    @staticmethod
    def get_nam_provincia(instance):
        departamento = Departamento.objects.filter(in1=instance.departamento)
        if departamento.exists():
            return departamento.first().provincia_in1.nam
        return instance.departamento[:2]


class LetraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letra
        fields = ('letra', 'letra_desc',)


class CLAE2Serializer(serializers.ModelSerializer):
    cantidad_por_provincia = serializers.SerializerMethodField()

    class Meta:
        model = CLAE2
        fields = ('letra', 'clae2', 'clae2_desc', 'cantidad_por_provincia',)

    @staticmethod
    def get_cantidad_por_provincia(instance):
        return EstablecimientoProductivo.objects.filter(clae2=instance).annotate(
            provincia=Substr("departamento", 1, 2)).values("provincia").annotate(
            cantidad=Count('clae2'))


class EstudioUniversitarioSerializer(serializers.ModelSerializer):
    rama_id = serializers.CharField(source="rama.id", read_only=True)
    rama = serializers.CharField(source="rama.nombre", read_only=True)
    area_id = serializers.CharField(source="area.id", read_only=True)
    area = serializers.CharField(source="area.descripcion", read_only=True)

    class Meta:
        model = EstudioUniversitario
        fields = ('id', 'rama_id', 'rama', 'area_id', 'area',)


class EstudioNoUniversitarioSerializer(serializers.ModelSerializer):
    area_id = serializers.CharField(source="area.id", read_only=True)
    area = serializers.CharField(source="area.descripcion", read_only=True)
    rama_id = serializers.CharField(source="rama.id", read_only=True)
    rama = serializers.CharField(source="rama.nombre", read_only=True)

    class Meta:
        model = EstudioNoUniversitario
        fields = ('id', 'area_id', 'area', 'rama_id', 'rama',)


class TipoGestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestion
        fields = ('id', 'descripcion',)


class EmpleoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimensionEmpresa
        fields = ('id', 'descripcion',)


class TipoTituloSerializer(serializers.Serializer):
    id_tipo_titulo = serializers.IntegerField()
    descripcion_tipo_titulo = serializers.CharField()
    tipo_establecimiento = serializers.CharField()


class ProvinciaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Provincia
        geo_field = "geom"
        fields = ("in1", "nam", "gna", "fna",)
        auto_bbox = True


class DepartamentoSerializer(GeoFeatureModelSerializer):
    provincia_in1 = serializers.CharField(source="provincia_in1.nam", read_only=True)
    top_sector_productivo = serializers.SerializerMethodField()
    tasa_empleo_formal = serializers.SerializerMethodField()

    class Meta:
        model = Departamento
        geo_field = "geom"
        fields = ("provincia_in1", "nam", "gna", "fna", "top_sector_productivo", "tasa_empleo_formal",)
        auto_bbox = True

    @staticmethod
    def get_top_sector_productivo(instance):
        return (SectorMayoritario.objects.filter(departamento=instance)
                .values("sector").first().get("sector", None))

    @staticmethod
    def get_tasa_empleo_formal(instance):
        return (TasaEmpleoFormal.objects.filter(departamento=instance)
                .values("tasa_empleo").first().get("tasa_empleo", None))
