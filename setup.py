from setuptools import find_packages, setup


__version__ = "0.9.1+dev"

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
        "django",
        "django-cors-headers",
        "django-guardian",
        "django-health-check",
        "django-rest-registration",
        "django-ses",
        "djangorestframework",
        "djangorestframework-jwt",
        "drf_yasg",
        "jinja2",
        "psycopg2-binary",
        "pyyaml",
        "sentry-sdk",
        "tomlkit",
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
