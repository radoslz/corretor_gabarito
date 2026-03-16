from django import forms

from apps.schools.models import ClassGroup, Student
from .models import Exam, ExamApplication, StudentExamResult, StudentAnswer


class BaseStyledModelForm(forms.ModelForm):
    """Form base para aplicar classes CSS padrão nos campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            css_class = "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                css_class = "form-select"
            field.widget.attrs.setdefault("class", css_class)


class ExamForm(BaseStyledModelForm):
    class Meta:
        model = Exam
        fields = [
            "title",
            "subject",
            "application_date",
            "question_count",
            "max_score",
            "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Ex.: SEAMA Matemática 2º ano"}),
            "application_date": forms.DateInput(attrs={"type": "date"}),
            "question_count": forms.NumberInput(attrs={"min": 1, "max": 100}),
            "max_score": forms.NumberInput(attrs={"step": "0.01", "min": 0}),
        }


class ExamApplicationForm(BaseStyledModelForm):
    class Meta:
        model = ExamApplication
        fields = ["exam", "class_group", "notes", "is_active"]
        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Observações opcionais sobre a aplicação da prova"
                }
            ),
        }


class ExamApplicationCreateForm(BaseStyledModelForm):
    """
    Form útil para associar uma prova já criada a uma turma.
    Pode ser usado numa tela específica de 'aplicar prova'.
    """

    class Meta:
        model = ExamApplication
        fields = ["class_group", "notes", "is_active"]
        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Observações opcionais sobre a aplicação da prova"
                }
            ),
        }


class MultiClassGroupExamApplicationForm(forms.Form):
    """
    Form para associar a mesma prova a várias turmas de uma vez.
    """
    class_groups = forms.ModelMultipleChoiceField(
        queryset=ClassGroup.objects.filter(is_active=True).order_by(
            "-school_year", "grade_level", "name"
        ),
        label="turmas",
        widget=forms.CheckboxSelectMultiple,
    )
    notes = forms.CharField(
        label="observações",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
    )
    is_active = forms.BooleanField(
        label="ativo",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class ExamCorrectionFilterForm(forms.Form):
    exam_application = forms.ModelChoiceField(
        queryset=ExamApplication.objects.filter(is_active=True).select_related(
            "exam", "class_group"
        ),
        label="aplicação da prova",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.filter(is_active=True).select_related("class_group"),
        label="aluno",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class StudentExamResultForm(BaseStyledModelForm):
    class Meta:
        model = StudentExamResult
        fields = ["student"]

    def __init__(self, *args, **kwargs):
        exam_application = kwargs.pop("exam_application", None)
        super().__init__(*args, **kwargs)

        if exam_application:
            self.fields["student"].queryset = exam_application.class_group.students.filter(
                is_active=True
            )

        self.fields["student"].widget.attrs.setdefault("class", "form-select")


class StudentAnswerForm(BaseStyledModelForm):
    class Meta:
        model = StudentAnswer
        fields = ["question_number", "is_correct"]
        widgets = {
            "question_number": forms.NumberInput(attrs={"readonly": "readonly"}),
        }