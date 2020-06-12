from django.contrib import admin
from django.urls import path, include


from apps.job_scripts import urls as job_script_urls



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
]
