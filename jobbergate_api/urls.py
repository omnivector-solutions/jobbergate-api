from django.contrib import admin
from django.urls import path, include

from apps.registries import urls as registry_urls

from apps.job_scripts import urls as job_script_urls

from apps.job_submissions import urls as job_submit_urls


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
        'registries/',
        include(registry_urls),
    ),
    path(
        'job-scripts/',
        include(job_script_urls),
    ),
    path(
        'job-submissions/',
        include(job_submit_urls),
    ),
]
