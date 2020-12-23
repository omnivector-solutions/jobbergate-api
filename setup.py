from setuptools import find_packages, setup


setup(
    name="jobbergate-api",
    packages=find_packages(include=["jobbergate_api", "jobbergate_api.*"]),
    version="0.1.0+dev",
    license="MIT",
    long_description=open("README.md").read(),
    install_requires=[
        "boto3",
        "click",
        "codado",
        "django",
        "django-cors-headers",
        "django-guardian",
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
            "tox",
            "wheel",
        ],
    },
)
