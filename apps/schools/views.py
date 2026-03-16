import csv
from io import TextIOWrapper

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import ClassGroupForm, SchoolForm, StudentForm, StudentImportForm
from .models import ClassGroup, School, Student


@login_required
def school_list_view(request):
    schools = School.objects.all().order_by("name")
    return render(request, "schools/school_list.html", {"schools": schools})


@login_required
def school_create_view(request):
    if request.method == "POST":
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Escola cadastrada com sucesso.")
            return redirect("schools:school_list")
    else:
        form = SchoolForm()

    return render(request, "schools/school_form.html", {"form": form, "title": "Nova escola"})


@login_required
def class_group_list_view(request):
    class_groups = (
        ClassGroup.objects.select_related("school", "responsible_teacher")
        .all()
        .order_by("-school_year", "grade_level", "name")
    )
    return render(request, "schools/classgroup_list.html", {"class_groups": class_groups})


@login_required
def class_group_create_view(request):
    if request.method == "POST":
        form = ClassGroupForm(request.POST)
        if form.is_valid():
            class_group = form.save(commit=False)
            if not class_group.responsible_teacher:
                class_group.responsible_teacher = request.user
            class_group.save()
            messages.success(request, "Turma cadastrada com sucesso.")
            return redirect("schools:classgroup_list")
    else:
        form = ClassGroupForm(initial={"responsible_teacher": request.user})

    return render(request, "schools/classgroup_form.html", {"form": form, "title": "Nova turma"})


@login_required
def class_group_update_view(request, pk):
    class_group = get_object_or_404(ClassGroup, pk=pk)

    if request.method == "POST":
        form = ClassGroupForm(request.POST, instance=class_group)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada com sucesso.")
            return redirect("schools:classgroup_detail", pk=class_group.pk)
    else:
        form = ClassGroupForm(instance=class_group)

    return render(request, "schools/classgroup_form.html", {"form": form, "title": f"Editar turma: {class_group.name}"})


@login_required
def student_list_view(request):
    students = Student.objects.select_related("class_group", "class_group__school").all()
    selected_school_id = request.GET.get("school", "")
    selected_school_year = request.GET.get("school_year", "")
    selected_class_group_id = request.GET.get("class_group", "")

    if selected_school_id:
        students = students.filter(class_group__school_id=selected_school_id)

    if selected_school_year:
        students = students.filter(class_group__school_year=selected_school_year)

    if selected_class_group_id:
        students = students.filter(class_group_id=selected_class_group_id)

    students = students.order_by(
        "class_group__school_year", "class_group__grade_level", "class_group__name", "name"
    )

    class_groups = ClassGroup.objects.select_related("school").all().order_by("-school_year", "name")
    if selected_school_id:
        class_groups = class_groups.filter(school_id=selected_school_id)
    if selected_school_year:
        class_groups = class_groups.filter(school_year=selected_school_year)

    school_years = (
        ClassGroup.objects.order_by("-school_year")
        .values_list("school_year", flat=True)
        .distinct()
    )

    context = {
        "students": students,
        "schools": School.objects.all().order_by("name"),
        "school_years": school_years,
        "class_groups": class_groups,
        "selected_school_id": selected_school_id,
        "selected_school_year": selected_school_year,
        "selected_class_group_id": selected_class_group_id,
    }
    return render(request, "schools/student_list.html", context)


@login_required
def student_create_view(request):
    initial = {}
    class_group_id = request.GET.get("class_group")
    if class_group_id:
        initial["class_group"] = class_group_id

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Aluno cadastrado com sucesso.")
            return redirect("schools:student_list")
    else:
        form = StudentForm(initial=initial)

    return render(request, "schools/student_form.html", {"form": form, "title": "Novo aluno"})


@login_required
def student_update_view(request, pk):
    student = get_object_or_404(Student.objects.select_related("class_group"), pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Aluno atualizado com sucesso.")
            return redirect("schools:classgroup_detail", pk=student.class_group.pk)
    else:
        form = StudentForm(instance=student)

    return render(request, "schools/student_form.html", {"form": form, "title": f"Editar aluno: {student.name}"})


@login_required
def student_import_view(request):
    selected_class_group = None
    class_group_id = request.GET.get("class_group") or request.POST.get("class_group")
    if class_group_id:
        selected_class_group = get_object_or_404(ClassGroup, pk=class_group_id)

    next_url = request.GET.get("next") or request.POST.get("next") or ""
    if next_url and not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = ""

    if request.method == "POST":
        form = StudentImportForm(request.POST, request.FILES)
        if form.is_valid():
            class_group = form.cleaned_data["class_group"]
            uploaded_file = form.cleaned_data["file"]
            created_count = 0
            skipped_count = 0

            try:
                decoded_file = TextIOWrapper(uploaded_file.file, encoding="utf-8")
                reader = csv.reader(decoded_file)

                for row in reader:
                    if not row:
                        continue

                    raw_name = row[0].strip()
                    if not raw_name:
                        continue

                    try:
                        Student.objects.create(
                            class_group=class_group,
                            name=raw_name,
                        )
                        created_count += 1
                    except IntegrityError:
                        skipped_count += 1

                messages.success(
                    request,
                    f"Importacao concluida. {created_count} aluno(s) criado(s) e {skipped_count} linha(s) ignorada(s).",
                )
                if next_url:
                    return redirect(next_url)
                return redirect("schools:classgroup_detail", pk=class_group.pk)

            except Exception as exc:
                messages.error(request, f"Erro ao importar arquivo: {exc}")
    else:
        initial = {}
        if selected_class_group:
            initial["class_group"] = selected_class_group.pk
        form = StudentImportForm(initial=initial)

    context = {
        "form": form,
        "title": "Importar alunos",
        "selected_class_group": selected_class_group,
        "next_url": next_url,
    }
    return render(request, "schools/student_import.html", context)


@login_required
def class_group_detail_view(request, pk):
    class_group = get_object_or_404(
        ClassGroup.objects.select_related("school", "responsible_teacher").prefetch_related("students"),
        pk=pk,
    )
    return render(request, "schools/classgroup_detail.html", {"class_group": class_group})
