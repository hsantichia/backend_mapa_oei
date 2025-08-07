from pathlib import Path

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView
from django.db.models import Model

import pandas as pd

from applications.ubicaciones.forms import ImportForm
from applications.ubicaciones.models import SectorMayoritario, Departamento, TasaEmpleoFormal


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
    def get_instance_from_id(df: pd.DataFrame, to_replace: str, instance: type[Model],
                             from_variable: str = None) -> pd.DataFrame:
        _to_find = from_variable if from_variable else "id"

        for x in df[to_replace].unique():
            obj = instance.objects.filter(**{_to_find: x}).first()
            df.loc[df[to_replace] == x, to_replace] = obj
        return df

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]
        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])


class SectorMayoritarioImportView(BulkImportView):
    model = SectorMayoritario
    extra_context = {"title": "Importación de sector mayoritario"}

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]
        df = self.get_instance_from_id(df, "departamento", Departamento, "in1")
        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])


class TasaEmpleoFormalImportView(BulkImportView):
    model = TasaEmpleoFormal
    extra_context = {"title": "Importación de tasa de empleo formal por departamento"}

    def insert_to_db(self, df: pd.DataFrame) -> None:
        _col = self.model.get_columns()
        if "id" in df.columns:
            _col.append("id")
        df = df[_col]
        df = self.get_instance_from_id(df, "departamento", Departamento, "in1")
        data_to_insert = df.to_dict(orient='records')
        self.model.objects.bulk_create([self.model(**data) for data in data_to_insert])
