from django import forms

from .models import School, ClassGroup, Student


class BaseStyledModelForm(forms.ModelForm):
    """Form base para aplicar classes CSS padrão nos campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                css_class = "form-select"
            field.widget.attrs.setdefault("class", css_class)


class SchoolForm(BaseStyledModelForm):
    class Meta:
        model = School
        fields = ["name", "city", "state", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ex.: C. E. Hosano Gomes Ferreira"}),
            "city": forms.TextInput(attrs={"placeholder": "Ex.: Lago dos Rodrigues"}),
            "state": forms.TextInput(attrs={"placeholder": "Ex.: MA", "maxlength": 2}),
        }


class ClassGroupForm(BaseStyledModelForm):
    class Meta:
        model = ClassGroup
        fields = [
            "school",
            "name",
            "grade_level",
            "shift",
            "school_year",
            "responsible_teacher",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ex.: 3º A"}),
            "school_year": forms.NumberInput(attrs={"min": 2024, "max": 2100}),
        }


class StudentForm(BaseStyledModelForm):
    class Meta:
        model = Student
        fields = ["class_group", "name", "registration_number", "notes", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Nome completo do aluno"}),
            "registration_number": forms.TextInput(attrs={"placeholder": "Opcional"}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Observações opcionais"}),
        }


class StudentImportForm(forms.Form):
    class_group = forms.ModelChoiceField(
        queryset=ClassGroup.objects.filter(is_active=True),
        label="turma",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    file = forms.FileField(
        label="arquivo CSV",
        help_text="Envie um arquivo .csv com um nome por linha ou com a primeira coluna contendo os nomes.",
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".csv,.txt"}),
    )