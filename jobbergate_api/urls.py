from django.contrib import admin
from django.urls import path, include

from apps.job_script import urls as job_script_urls
from apps.job_submission import urls as job_submission_urls
from apps.application import urls as application_urls


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'api-auth/',
        include('rest_framework.urls')
    ),
    path(
        'job-scripts/',
        include(job_script_urls),
    ),
    path(
        'job-submission/',
        include(job_submission_urls),
    ),
    path(
        'job-scripts/',
        include(application_urls),
    ),
]
