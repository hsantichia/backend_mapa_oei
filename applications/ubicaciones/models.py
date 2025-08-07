from django.contrib.gis.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_columns(cls):
        columns = [field.name for field in cls._meta.local_fields]
        columns.remove("id")
        return columns


class Provincia(models.Model):
    in1 = models.CharField("Código INDEC", primary_key=True, max_length=2, null=False, blank=False)
    geom = models.MultiPolygonField("Geometría", dim=2, srid=4326)
    entidad = models.IntegerField("Código que hace referencia al objeto geográfico", null=True, blank=True)
    objeto = models.CharField("Tipo de objeto geográfico", max_length=50, null=True, blank=True)
    fna = models.CharField("Nombre geográfico", max_length=120, null=False, blank=False)
    nam = models.CharField("Nombre de la provincia", max_length=60, null=False, blank=False)
    gna = models.CharField("Término genérico", max_length=70, null=False, blank=False)
    fdc = models.CharField("Fuente de captura", max_length=120, null=True, blank=True)
    sag = models.CharField("Autoridad de fuente", max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"

    def __str__(self):
        return self.nam


class Departamento(models.Model):
    in1 = models.CharField("Código INDEC", primary_key=True, max_length=5, null=False, blank=False)
    geom = models.MultiPolygonField("Geometría", dim=2, srid=4326)
    objeto = models.CharField("Tipo de objeto geográfico", max_length=50, null=True, blank=True)
    fna = models.CharField("Nombre geográfico", max_length=120, null=False, blank=False)
    nam = models.CharField("Nombre del departamento", max_length=80, null=False, blank=False)
    gna = models.CharField("Término genérico", max_length=70, null=False, blank=False)
    fdc = models.CharField("Fuente de captura", max_length=120, null=True, blank=True)
    sag = models.CharField("Autoridad de fuente", max_length=30, null=True, blank=True)
    provincia_in1 = models.ForeignKey(Provincia, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nam


class LimiteInterprovincial(models.Model):
    gid = models.PositiveIntegerField("Geometría ID", primary_key=True, null=False, blank=False)
    geom = models.MultiLineStringField("Geometría", dim=2, srid=4326)
    entidad = models.IntegerField("Código que hace referencia al objeto geográfico", null=True, blank=True)
    objeto = models.CharField("Tipo de objeto geográfico", max_length=50, null=True, blank=True)
    fna = models.CharField("Nombre geográfico", max_length=120, null=False, blank=False)
    nam = models.CharField("Término específico", max_length=50, null=False, blank=False)
    gna = models.CharField("Término genérico", max_length=70, null=False, blank=False)
    vlj = models.FloatField("Validación de límite interprovincial", null=True, blank=True)
    fdc = models.CharField("Fuente de captura", max_length=120, null=True, blank=True)
    sag = models.CharField("Autoridad de fuente", max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = 'Límite interprovincial'
        verbose_name_plural = 'Límites interprovinciales'

    def __str__(self):
        return self.fna


class SectorMayoritario(BaseModel):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='sectores')
    sector = models.CharField('Sector', max_length=2, null=False, blank=False)

    class Meta:
        verbose_name = "Sector Mayoritario"
        verbose_name_plural = "Sectores Mayoritarios"

    def __str__(self):
        return self.departamento


class TasaEmpleoFormal(BaseModel):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='empleo')
    tasa_empleo = models.FloatField('Tasa de empleo formal', null=False, blank=False)

    class Meta:
        verbose_name = "Tasa de empleo formal"
        verbose_name_plural = "Tasas de empleo formal"

    def __str__(self):
        return self.departamento
