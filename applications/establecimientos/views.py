from pathlib import Path

import pandas as pd
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import FormView

from .forms import ImportForm
from .models import Universidad, Facultad, Rama, AreaDeEstudio, Titulo, EstablecimientoNoUniversitario, Letra, \
    EstablecimientoProductivo, DimensionEmpresa, CLAE2, Gestion, TipoTitulo, Escuela, BaseModel, UnidadMedida, \
    EstablecimientoUniversitario, EstudioNoUniversitario, EstudioUniversitario


class BulkImportView(PermissionRequiredMixin, FormView):
    permission_required = 'is_staff'

    template_name = 'importacion_masiva.html'
    form_class = ImportForm
    success_url = "."

    model = None

    def get_context_data(self, **kwargs):
        context = super(BulkImportView, self).get_context_data(**kwargs)
        context["mensaje_exitoso"] = False
        context["mensaje_error"] = False
        context["columns"] = self.model.get_columns()
        return context

    def form_valid(self, form):
        archivo = self.request.FILES['archivo']
        extension = Path(str(archivo)).suffix
        context = self.get_context_data()

        try:
            df = self.importar_desde_archivo(archivo, extension)
            self.insert_to_db(df)
            context["mensaje_exito"] = "Proceso de importación realizado exitosamente"
        except Exception as error:
            context["mensaje_error"] = error

        super().form_valid(form)
        return self.render_to_response(context)

    @staticmethod
    def importar_desde_archivo(archivo, archivo_formato):
        if archivo_formato == '.csv':
            df = pd.read_csv(archivo)
        elif archivo_formato in ['.xlsx', '.xls']:
            df = pd.read_excel(archivo)
        else:
            raise ValueError("Formato de archivo no válido")

        return df

    @staticmethod
    def get_instance_from_id(df: pd.DataFrame, to_replace: str, instance: type[BaseModel],
                             from_variable: str = None) -> pd.DataFrame:
        _to_find = from_variable if from_variable else "id"

        for x in df[to_replace].unique():
            obj = instance.objects.filter(**{_to_find: int(x)}).first()
            df.loc[df[to_replace] == x, to_replace] = obj
        return df

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]
        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])


class TipoTituloImportView(BulkImportView):
    model = TipoTitulo
    extra_context = {"title": "Importación de tipo de títulos para establecimientos educativos"}


class TituloImportView(BulkImportView):
    model = Titulo
    extra_context = {"title": "Importación de títulos de los establecimientos educativos"}

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]
        df = self.get_instance_from_id(df, "tipo", TipoTitulo)
        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])


class GestionImportView(BulkImportView):
    model = Gestion
    extra_context = {"title": "Importación de tipo de gestión"}


class UnidadMedidaImportView(BulkImportView):
    model = UnidadMedida
    extra_context = {"title": "Importación de unidad de medida"}


class AreaDeEstudioImportView(BulkImportView):
    model = AreaDeEstudio
    extra_context = {"title": "Importación de áreas de estudio"}


class RamaImportView(BulkImportView):
    model = Rama
    extra_context = {"title": "Importación de ramas de estudio"}


class EstudioUniversitarioImportView(BulkImportView):
    model = EstudioUniversitario
    extra_context = {"title": "Importación de area y rama de estudio para establecimientos universitarios"}

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]
        df = self.get_instance_from_id(df, "rama", Rama)
        df = self.get_instance_from_id(df, "area", AreaDeEstudio)
        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])


class EstudioNoUniversitarioImportView(BulkImportView):
    model = EstudioNoUniversitario
    extra_context = {"title": "Importación de area de estudio para establecimientos no universitarios"}

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]
        df = self.get_instance_from_id(df, "rama", Rama)
        df = self.get_instance_from_id(df, "area", AreaDeEstudio)
        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])


class LetraImportView(BulkImportView):
    model = Letra
    extra_context = {"title": "Importación de Clasificaciones de Actividad Económica (CLAE) a nivel de letra"}


class CLAE2ImportView(BulkImportView):
    model = CLAE2
    extra_context = {"title": "Importación de Clasificaciones de Actividad Económica (CLAE) a 2 dígitos"}

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]
        df = self.get_instance_from_id(df, "letra", Letra, "letra")
        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])


class DimensionEmpresaImportView(BulkImportView):
    model = DimensionEmpresa
    extra_context = {"title": "Importación de tamaños de empresa"}


class UniversidadImportView(BulkImportView):
    model = Universidad
    extra_context = {"title": "Importación de universidades"}


class FacultadImportView(BulkImportView):
    model = Facultad
    extra_context = {"title": "Importación de facultades"}


class EstablecimientoUniversitarioImportView(BulkImportView):
    model = EstablecimientoUniversitario
    extra_context = {"title": "Importación de establecimientos universitarios"}

    @staticmethod
    def get_instance_from_id(df: pd.DataFrame, to_replace: str, instance: type[BaseModel],
                             from_variable: str = None) -> pd.DataFrame:
        _to_find = from_variable if from_variable else "id"

        for x in df[to_replace].unique():
            obj = instance.objects.filter(**{_to_find: x}).first()
            df.loc[df[to_replace] == x, to_replace] = obj
        return df

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        _col.remove("lat_lon")
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]

        self.get_instance_from_id(df, "universidad", Universidad)
        self.get_instance_from_id(df, "facultad", Facultad)
        self.get_instance_from_id(df, "gestion", Gestion)
        self.get_instance_from_id(df, "titulo", Titulo)
        self.get_instance_from_id(df, "tipo_titulo", TipoTitulo)
        self.get_instance_from_id(df, "unidad_medida", UnidadMedida)
        self.get_instance_from_id(df, "rama", Rama)
        self.get_instance_from_id(df, "area", AreaDeEstudio)

        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])


class EscuelaImportView(BulkImportView):
    model = Escuela
    extra_context = {"title": "Importación de escuelas"}


class EstablecimientoNoUniversitarioImportView(BulkImportView):
    model = EstablecimientoNoUniversitario
    extra_context = {"title": "Importación de establecimientos no universitarios"}

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        _col.remove("lat_lon")
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]

        self.get_instance_from_id(df, "escuela", Escuela)
        self.get_instance_from_id(df, "gestion", Gestion)
        self.get_instance_from_id(df, "titulo", Titulo)
        self.get_instance_from_id(df, "rama", Rama)
        self.get_instance_from_id(df, "area", AreaDeEstudio)

        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])


class EstablecimientoProductivoImportView(BulkImportView):
    model = EstablecimientoProductivo
    extra_context = {"title": "Importación de establecimientos productivos"}

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        _col.remove("lat_lon")
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]

        self.get_instance_from_id(df, "empleo", DimensionEmpresa)
        self.get_instance_from_id(df, "clae2", CLAE2, "clae2")

        data_to_insert = df.to_dict(orient='records')
        for data in data_to_insert:
            self.model.objects.create(**data)
