from setuptools import find_packages, setup


__version__ = "0.11.2+dev"

setup(
    name="jobbergate-api",
    packages=find_packages(include=["jobbergate_api", "jobbergate_api.*"]),
    version=__version__,
    license="MIT",
    long_description=open("README.md").read(),
    install_requires=[
        "boto3",
        "click",
        "codado",
        "django<=3.1.8",
        "django-cors-headers",
        "django-guardian",
        "django-health-check",
        "django-rest-registration",
        "django-ses",
        "djangorestframework",
        "djangorestframework-jwt",
        "drf_yasg",
        "jinja2",
        "idna==2.10",
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
