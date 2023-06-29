from django import forms

class ExcelInput(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            widget_attrs = field.widget.attrs
            widget_attrs['class'] = 'form-control mb-3 mt-1'
            widget_attrs['class'] = 'form-control mb-3 mt-1'

    files = forms.FileField()

    def clean_files(self):
        file = self.cleaned_data['files']
        if 'xlsx' not in file.name or 'xls' not in file.name:
            raise forms.ValidationError(f'O arquivo "{file}" não está no formato excel')