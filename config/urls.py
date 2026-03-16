from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("exams:dashboard")
    return redirect("accounts:login")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    path("schools/", include(("apps.schools.urls", "schools"), namespace="schools")),
    path("exams/", include(("apps.exams.urls", "exams"), namespace="exams")),
    path("", root_redirect, name="root"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)