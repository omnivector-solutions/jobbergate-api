import datetime
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# REQUIRED environment variables
SERVERLESS_STAGE = os.environ["STAGE"]
REGISTER_VERIFICATION_URL = os.environ["REGISTER_VERIFICATION_URL"]


# OPTIONAL environment variables
SENTRY_DSN = os.getenv("SENTRY_DSN")
IS_OFFLINE = os.getenv("LAMBDA_TASK_ROOT") is None  # the serverless runtime sets this


# settings when running locally (no serverless runtime)
if IS_OFFLINE:
    # Database
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.0/howto/static-files/
    STATIC_URL = "/static/"

else:  # serverless runtime
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DATABASE_NAME"],
            "USER": os.environ["DATABASE_USER"],
            "PASSWORD": os.environ["DATABASE_PASS"],
            "HOST": os.environ["DATABASE_HOST"],
            "PORT": os.environ["DATABASE_PORT"],
        }
    }

    STATIC_URL = "https://{}/".format(os.environ["CLOUDFRONT_DOMAIN"])


if SENTRY_DSN:
    import sentry_sdk  # noqa
    from sentry_sdk.integrations.django import DjangoIntegration  # noqa

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )


S3_BUCKET = f"jobbbergate-api-{SERVERLESS_STAGE}-resources"

S3_BASE_PATH = "jobbergate-resources"

TAR_NAME = "/tmp/jobbergate/jobbergate.tar.gz"

APPLICATION_FILE = "/tmp/jobbergate/jobbergate.py"

CONFIG_FILE = "/tmp/jobbergate/jobbergate.yaml"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "z%bhg09ma4_h^ps0&bxizvkis0vj0^1rwhs!c0)2f6_^8c#dbt"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [  # Warning: The order that these get loaded matters, don't reorder
    "drf_yasg",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "rest_registration",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",
    "apps.user",
    "apps.job_scripts",
    "apps.job_submissions",
    "apps.applications",
]

AUTHENTICATION_BACKENDS = (  # Warning: The order that these get loaded matters, don't reorder
    "django.contrib.auth.backends.ModelBackend",  # default
    "guardian.backends.ObjectPermissionBackend",
)

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [  # Warning: The order that these get loaded matters, don't reorder
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "jobbergate_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "jobbergate_api.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {"NAME": "jobbergate_api.password_validation.ASCIIRegexValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_ROOT = "static/"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# RestFramework Settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

# REST_USE_JWT = True

AUTH_USER_MODEL = "user.User"

JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=900),
}

REST_REGISTRATION = {
    "REGISTER_VERIFICATION_ENABLED": True,
    "REGISTER_EMAIL_VERIFICATION_ENABLED": False,
    "RESET_PASSWORD_VERIFICATION_ENABLED": False,
    "VERIFICATION_FROM_EMAIL": "info@omnivector.solutions",
    "REGISTER_VERIFICATION_URL": REGISTER_VERIFICATION_URL,
}


EMAIL_BACKEND = "django_ses.SESBackend"
