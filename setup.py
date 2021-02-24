from setuptools import find_packages, setup


__version__ = "0.10.0+dev"

setup(
    name="jobbergate-api",
    packages=find_packages(include=["jobbergate_api", "jobbergate_api.*", "apps", "apps.*"]),
    version=__version__,
    license="MIT",
    long_description=open("README.md").read(),
    install_requires=[
        "boto3",
        "click",
        "codado",
        "django",
        "django-cors-headers",
        "django-guardian",
        "django-health-check",
        "django-rest-registration",
        "django-ses",
        "django-storages",
        "djangorestframework",
        "djangorestframework-jwt",
        "drf_yasg",
        "jinja2",
        "psycopg2-binary",
        "pyyaml",
        "sentry-sdk",
        "toml",
        "werkzeug",  # soft-required by the serverless lambda
    ],
    extras_require={
        "dev": [
            "black",
            "coverage",
            "flake8",
            "isort",
            "pytest",
            "pytest-cov",
            "pytest-django",
            "tox",
            "wheel",
        ],
    },
)
