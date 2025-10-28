from django.urls import include, path

urlpatterns = [
    path("", include("vcf.urls")),
]
