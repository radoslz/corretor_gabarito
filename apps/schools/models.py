from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        abstract = True


class School(TimeStampedModel):
    name = models.CharField("nome", max_length=150)
    city = models.CharField("cidade", max_length=100, blank=True)
    state = models.CharField("estado", max_length=2, blank=True)
    is_active = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "escola"
        verbose_name_plural = "escolas"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ClassGroup(TimeStampedModel):
    SHIFT_CHOICES = [
        ("matutino", "Matutino"),
        ("vespertino", "Vespertino"),
        ("noturno", "Noturno"),
        ("integral", "Integral"),
    ]

    GRADE_LEVEL_CHOICES = [
        ("1EM", "1º ano do Ensino Médio"),
        ("2EM", "2º ano do Ensino Médio"),
        ("3EM", "3º ano do Ensino Médio"),
    ]

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="class_groups",
        verbose_name="escola",
    )
    name = models.CharField("nome da turma", max_length=50)
    grade_level = models.CharField("série/ano", max_length=3, choices=GRADE_LEVEL_CHOICES)
    shift = models.CharField("turno", max_length=20, choices=SHIFT_CHOICES)
    school_year = models.PositiveIntegerField("ano letivo")
    responsible_teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responsible_classes",
        verbose_name="professor responsável",
    )
    is_active = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "turma"
        verbose_name_plural = "turmas"
        ordering = ["-school_year", "grade_level", "name"]
        unique_together = ("school", "name", "school_year")

    def __str__(self):
        return f"{self.name} - {self.get_grade_level_display()} ({self.school_year})"


class Student(TimeStampedModel):
    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name="turma",
    )
    name = models.CharField("nome", max_length=150)
    registration_number = models.CharField("matrícula", max_length=50, blank=True)
    notes = models.TextField("observações", blank=True)
    is_active = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "aluno"
        verbose_name_plural = "alunos"
        ordering = ["name"]
        unique_together = ("class_group", "name")

    def __str__(self):
        return self.name