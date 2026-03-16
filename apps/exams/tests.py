from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.exams.models import Exam, ExamApplication, StudentAnswer, StudentExamResult
from apps.schools.models import ClassGroup, School, Student

User = get_user_model()


class ExamReportViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="123456")
        self.client.force_login(self.user)

        self.school = School.objects.create(name="Escola A")
        self.class_group_a = ClassGroup.objects.create(
            school=self.school,
            name="3A",
            grade_level="3EM",
            shift="matutino",
            school_year=2026,
            responsible_teacher=self.user,
        )
        self.class_group_b = ClassGroup.objects.create(
            school=self.school,
            name="3B",
            grade_level="3EM",
            shift="vespertino",
            school_year=2026,
            responsible_teacher=self.user,
        )

        self.student_a = Student.objects.create(class_group=self.class_group_a, name="Ana")
        self.student_b = Student.objects.create(class_group=self.class_group_b, name="Bruno")

        self.exam = Exam.objects.create(
            title="Simulado",
            subject="matematica",
            application_date="2026-03-10",
            question_count=2,
            max_score=Decimal("10.00"),
            created_by=self.user,
        )
        self.application_a = ExamApplication.objects.create(exam=self.exam, class_group=self.class_group_a)
        self.application_b = ExamApplication.objects.create(exam=self.exam, class_group=self.class_group_b)

        self.result_a = StudentExamResult.objects.create(
            exam_application=self.application_a,
            student=self.student_a,
            total_correct=2,
            score=Decimal("10.00"),
            percentage=Decimal("100.00"),
            corrected_by=self.user,
        )
        self.result_b = StudentExamResult.objects.create(
            exam_application=self.application_b,
            student=self.student_b,
            total_correct=1,
            score=Decimal("5.00"),
            percentage=Decimal("50.00"),
            corrected_by=self.user,
        )

        StudentAnswer.objects.create(result=self.result_a, question_number=1, is_correct=True)
        StudentAnswer.objects.create(result=self.result_a, question_number=2, is_correct=True)
        StudentAnswer.objects.create(result=self.result_b, question_number=1, is_correct=True)
        StudentAnswer.objects.create(result=self.result_b, question_number=2, is_correct=False)

    def test_exam_report_shows_all_results_by_default(self):
        response = self.client.get(reverse("exams:exam_report", args=[self.exam.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student_a.name)
        self.assertContains(response, self.student_b.name)

    def test_exam_report_filters_by_application(self):
        response = self.client.get(
            reverse("exams:exam_report", args=[self.exam.pk]),
            {"application_id": self.application_a.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student_a.name)
        self.assertNotContains(response, self.student_b.name)
        self.assertEqual(response.context["selected_application"], self.application_a)


class CorrectionFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="123456")
        self.client.force_login(self.user)

        self.school = School.objects.create(name="Escola A")
        self.class_group = ClassGroup.objects.create(
            school=self.school,
            name="1A",
            grade_level="1EM",
            shift="matutino",
            school_year=2026,
            responsible_teacher=self.user,
        )
        self.student = Student.objects.create(class_group=self.class_group, name="Ana")
        self.exam = Exam.objects.create(
            title="Diagnostica",
            subject="matematica",
            application_date="2026-03-10",
            question_count=2,
            max_score=Decimal("10.00"),
            created_by=self.user,
        )
        self.application = ExamApplication.objects.create(exam=self.exam, class_group=self.class_group)

    def test_save_and_back_redirects_to_student_selection(self):
        response = self.client.post(
            reverse("exams:correction_student", args=[self.application.pk, self.student.pk]),
            {
                "action": "save_and_back",
                "question_1": "1",
                "question_2": "0",
            },
        )

        self.assertRedirects(response, reverse("exams:correction_select_student", args=[self.application.pk]))

    def test_student_selection_marks_corrected_students(self):
        StudentExamResult.objects.create(
            exam_application=self.application,
            student=self.student,
            total_correct=1,
            score=Decimal("5.00"),
            percentage=Decimal("50.00"),
            corrected_by=self.user,
        )

        response = self.client.get(reverse("exams:correction_select_student", args=[self.application.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corrigido")
