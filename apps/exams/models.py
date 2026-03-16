from django.db import models
from django.contrib.auth import get_user_model

from apps.schools.models import ClassGroup, Student

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        abstract = True


class Exam(TimeStampedModel):
    SUBJECT_CHOICES = [
        ("matematica", "Matemática"),
        ("portugues", "Português"),
        ("biologia", "Biologia"),
        ("fisica", "Física"),
        ("quimica", "Química"),
        ("historia", "História"),
        ("geografia", "Geografia"),
        ("ingles", "Inglês"),
        ("outra", "Outra"),
    ]

    title = models.CharField("título", max_length=150)
    subject = models.CharField(
        "disciplina",
        max_length=20,
        choices=SUBJECT_CHOICES,
        default="matematica",
    )
    application_date = models.DateField("data da aplicação")
    question_count = models.PositiveIntegerField("quantidade de questões")
    max_score = models.DecimalField("nota máxima", max_digits=5, decimal_places=2, default=10)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_exams",
        verbose_name="criado por",
    )
    is_active = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "prova"
        verbose_name_plural = "provas"
        ordering = ["-application_date", "title"]

    def __str__(self):
        return self.title


class ExamApplication(TimeStampedModel):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="prova",
    )
    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE,
        related_name="exam_applications",
        verbose_name="turma",
    )
    notes = models.TextField("observações", blank=True)
    is_active = models.BooleanField("ativo", default=True)

    class Meta:
        verbose_name = "aplicação da prova"
        verbose_name_plural = "aplicações da prova"
        ordering = [
            "class_group__school_year",
            "class_group__grade_level",
            "class_group__name",
        ]
        unique_together = ("exam", "class_group")

    def __str__(self):
        return f"{self.exam.title} - {self.class_group}"


class StudentExamResult(TimeStampedModel):
    exam_application = models.ForeignKey(
        ExamApplication,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="aplicação da prova",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="exam_results",
        verbose_name="aluno",
    )
    total_correct = models.PositiveIntegerField("total de acertos", default=0)
    score = models.DecimalField("nota", max_digits=6, decimal_places=2, default=0)
    percentage = models.DecimalField("percentual", max_digits=5, decimal_places=2, default=0)
    corrected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="corrected_results",
        verbose_name="corrigido por",
    )
    corrected_at = models.DateTimeField("corrigido em", null=True, blank=True)

    class Meta:
        verbose_name = "resultado da prova"
        verbose_name_plural = "resultados das provas"
        ordering = ["student__name"]
        unique_together = ("exam_application", "student")

    def __str__(self):
        return f"{self.student.name} - {self.exam_application.exam.title}"


class StudentAnswer(TimeStampedModel):
    result = models.ForeignKey(
        StudentExamResult,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="resultado",
    )
    question_number = models.PositiveIntegerField("número da questão")
    is_correct = models.BooleanField("acertou", default=False)

    class Meta:
        verbose_name = "resposta do aluno"
        verbose_name_plural = "respostas dos alunos"
        ordering = ["question_number"]
        unique_together = ("result", "question_number")

    def __str__(self):
        return f"{self.result.student.name} - Q{self.question_number}"