from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from .managers import TipoTituloManager


class BaseModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_columns(cls):
        columns = [field.name for field in cls._meta.local_fields]
        columns.remove("id")
        return columns


class Letra(BaseModel):
    letra = models.CharField("Letra", max_length=1, null=False, blank=False, unique=True)
    letra_desc = models.CharField("Descripción de la letra", max_length=120, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "CLAE a nivel letra"
        verbose_name_plural = "CLAEs a nivel letra"

    def __str__(self):
        return self.letra_desc


class CLAE2(BaseModel):
    letra = models.ForeignKey(Letra, on_delete=models.CASCADE)
    clae2 = models.PositiveIntegerField("ID de clae 2", null=False, blank=False, unique=True)
    clae2_desc = models.CharField("Descripción del clae a 2 dígitos", max_length=160, unique=True)

    class Meta:
        verbose_name = "CLAE a 2 dígitos"
        verbose_name_plural = "CLAEs a 2 dígitos"

    def __str__(self):
        return self.clae2_desc


class DimensionEmpresa(BaseModel):
    descripcion = models.CharField("Rango del tamaño de la empresa", null=False, blank=False, max_length=50)

    class Meta:
        verbose_name = "Tamaño de la empresa"
        verbose_name_plural = "Tamaños de las empresas"

    def __str__(self):
        return self.descripcion


class EstablecimientoProductivo(BaseModel):
    departamento = models.CharField("Código INDEC del departamento", max_length=5)
    empleo = models.ForeignKey(DimensionEmpresa, on_delete=models.CASCADE)
    clae2 = models.ForeignKey(CLAE2, on_delete=models.CASCADE)
    proporcion_mujeres = models.FloatField("Proporción de mujeres en la empresa", blank=True, null=True)
    lat = models.FloatField("Latitud", max_length=18)
    lon = models.FloatField("Longitud", max_length=18)
    lat_lon = models.PointField("Coordinada de ubicación", srid=4326, editable=False, null=True)

    class Meta:
        verbose_name = "Establecimiento Productivo"
        verbose_name_plural = "Establecimientos Productivos"

    def __str__(self):
        return f"{self.id}: {self.clae2} - {self.empleo}"

    def save(self, force_insert=False, force_update=True, using=None, update_fields=None):
        self.lat_lon = Point(x=self.lon, y=self.lat, srid=4326)
        super(EstablecimientoProductivo, self).save()


class TipoTitulo(BaseModel):
    descripcion = models.CharField("Tipo de título", blank=False, null=False, max_length=30)

    objects = TipoTituloManager()

    class Meta:
        verbose_name = "Tipo de título"
        verbose_name_plural = "Tipos de título"

    def __str__(self):
        return self.descripcion


class Titulo(BaseModel):
    tipo = models.ForeignKey(TipoTitulo, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre del título otorgado", max_length=150)

    class Meta:
        verbose_name = "Titulo"
        verbose_name_plural = "Titulos"

    def __str__(self):
        return f"{self.tipo}: {self.nombre}"


class Rama(BaseModel):
    """ Rama de estudio o Disciplina científica """
    nombre = models.CharField("Nombre de la rama", max_length=100)

    class Meta:
        verbose_name = "Rama"
        verbose_name_plural = "Ramas"

    def __str__(self):
        return self.nombre


class AreaDeEstudio(BaseModel):
    """ Área específica de estudio """
    descripcion = models.CharField("Descripción del área de estudio", max_length=160)

    class Meta:
        verbose_name = "Area de estudio"
        verbose_name_plural = "Areas de estudio"

    def __str__(self):
        return self.descripcion


class EstudioUniversitario(BaseModel):
    rama = models.ForeignKey(Rama, on_delete=models.CASCADE)
    area = models.ForeignKey(AreaDeEstudio, on_delete=models.CASCADE)

    def __str__(self):
        pass


class EstudioNoUniversitario(BaseModel):
    rama = models.ForeignKey(Rama, on_delete=models.CASCADE)
    area = models.ForeignKey(AreaDeEstudio, on_delete=models.CASCADE)

    def __str__(self):
        pass


class Universidad(BaseModel):
    nombre = models.CharField("Nombre de la universidad", max_length=100)

    class Meta:
        verbose_name = "Universidad"
        verbose_name_plural = "Universidades"

    def __str__(self):
        return self.nombre


class UnidadMedida(BaseModel):
    id = models.CharField("ID", max_length=1, primary_key=True, blank=False, null=False)
    descripcion = models.CharField("Unidad de medida", max_length=25, blank=False, null=False)

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"

    def __str__(self):
        return self.descripcion


class Gestion(BaseModel):
    descripcion = models.CharField("Descripción del tipo de gestión", max_length=20)

    class Meta:
        verbose_name = "Tipo de gestión"
        verbose_name_plural = "Tipo de gestiones"

    def __str__(self):
        return self.descripcion


class Facultad(BaseModel):
    nombre = models.CharField("Nombre de la Facultad", max_length=100)

    class Meta:
        verbose_name = "Facultad"
        verbose_name_plural = "Facultades"

    def __str__(self):
        return self.nombre


class EstablecimientoUniversitario(BaseModel):
    departamento = models.CharField("Código INDEC del departamento", max_length=5)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    tipo_titulo = models.ForeignKey(TipoTitulo, on_delete=models.CASCADE)
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    duracion = models.PositiveIntegerField("Duración de la carrera")
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    rama = models.ForeignKey(Rama, on_delete=models.CASCADE)
    area = models.ForeignKey(AreaDeEstudio, on_delete=models.CASCADE)
    lat = models.FloatField("Latitud", max_length=18)
    lon = models.FloatField("Longitud", max_length=18)
    lat_lon = models.PointField("Coordenada de ubicación", srid=4326, editable=False, null=True)

    class Meta:
        verbose_name = "Establecimiento universitario"
        verbose_name_plural = "Establecimientos universitarios"

    def __str__(self):
        return f"{self.universidad} {self.facultad}: {self.titulo}"

    def save(self, force_insert=False, force_update=True, using=None, update_fields=None):
        self.lat_lon = Point(x=self.lon, y=self.lat, srid=4326)
        super(EstablecimientoUniversitario, self).save()


class Escuela(BaseModel):
    nombre = models.CharField("Nombre del establecimiento", max_length=255)

    class Meta:
        verbose_name = "Escuela"
        verbose_name_plural = "Escuelas"

    def __str__(self):
        return self.nombre


class EstablecimientoNoUniversitario(BaseModel):
    departamento = models.CharField("Código INDEC del departamento", max_length=5)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    rama = models.ForeignKey(Rama, on_delete=models.CASCADE)
    area = models.ForeignKey(AreaDeEstudio, on_delete=models.CASCADE)
    lat = models.FloatField("Latitud", max_length=18)
    lon = models.FloatField("Longitud", max_length=18)
    lat_lon = models.PointField("Coordinada de ubicación", srid=4326, editable=False, null=True)

    class Meta:
        verbose_name = "Establecimiento no universitario"
        verbose_name_plural = "Establecimientos no universitarios"

    def __str__(self):
        return self.escuela.nombre

    def save(self, force_insert=False, force_update=True, using=None, update_fields=None):
        self.lat_lon = Point(x=self.lon, y=self.lat, srid=4326)
        super(EstablecimientoNoUniversitario, self).save()
