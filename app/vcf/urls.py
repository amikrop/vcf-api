from django.urls import path

from vcf.views import VCFView

urlpatterns = [
    path("", VCFView.as_view()),
]
