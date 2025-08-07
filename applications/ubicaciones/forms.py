from django import forms


class ImportForm(forms.Form):
    archivo = forms.FileField(widget=forms.FileInput(attrs={"class": "form-control"}))
