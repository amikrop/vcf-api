import os
import sys
from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env.str("SECRET_KEY", "secret-key")

DEBUG = env.bool("DEBUG", True)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "vcf",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "vcfapi.urls"

WSGI_APPLICATION = "vcfapi.wsgi.application"

TIME_ZONE = "UTC"

USE_I18N = False

USE_TZ = True

DEFAULT_PAGE_SIZE = 100

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework_xml.renderers.XMLRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": env.int("DJANGO_PAGE_SIZE", DEFAULT_PAGE_SIZE),
}

VCF_FILE_BASENAME = env.str("VCF_FILE_BASENAME", "variants.vcf")

VCF_FILE_PATH = env.str("VCF_FILE_PATH", BASE_DIR / "data" / VCF_FILE_BASENAME)

# Validate VCF file existence and permissions unless running tests
if "pytest" not in sys.modules:
    if not os.path.isfile(VCF_FILE_PATH):
        raise ImproperlyConfigured(f"VCF file does not exist: {VCF_FILE_PATH}")

    if not (os.access(VCF_FILE_PATH, os.R_OK) and os.access(VCF_FILE_PATH, os.W_OK)):
        raise ImproperlyConfigured(
            f"VCF file is not readable and writable: {VCF_FILE_PATH}"
        )

DEFAULT_WRITE_TOKEN = "secret-token"

WRITE_TOKEN = env.str("DJANGO_WRITE_TOKEN", DEFAULT_WRITE_TOKEN)
