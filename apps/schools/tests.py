from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.schools.models import ClassGroup, School, Student

User = get_user_model()


class StudentListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="123456")
        self.client.force_login(self.user)

        self.school_a = School.objects.create(name="Escola A")
        self.school_b = School.objects.create(name="Escola B")

        self.class_group_a = ClassGroup.objects.create(
            school=self.school_a,
            name="3A",
            grade_level="3EM",
            shift="matutino",
            school_year=2026,
            responsible_teacher=self.user,
        )
        self.class_group_b = ClassGroup.objects.create(
            school=self.school_b,
            name="2B",
            grade_level="2EM",
            shift="vespertino",
            school_year=2025,
            responsible_teacher=self.user,
        )

        self.student_a = Student.objects.create(class_group=self.class_group_a, name="Ana")
        self.student_b = Student.objects.create(class_group=self.class_group_b, name="Bruno")

    def test_student_list_shows_all_students_by_default(self):
        response = self.client.get(reverse("schools:student_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student_a.name)
        self.assertContains(response, self.student_b.name)

    def test_student_list_filters_by_school_year_and_class_group(self):
        response = self.client.get(
            reverse("schools:student_list"),
            {
                "school": self.school_a.pk,
                "school_year": self.class_group_a.school_year,
                "class_group": self.class_group_a.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student_a.name)
        self.assertNotContains(response, self.student_b.name)


class StudentImportViewTests(TestCase):
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

    def test_student_import_prefills_selected_class_group(self):
        response = self.client.get(
            reverse("schools:student_import"),
            {"class_group": self.class_group.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_class_group"], self.class_group)
        self.assertEqual(response.context["form"].initial["class_group"], self.class_group.pk)
