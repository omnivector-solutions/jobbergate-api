# from django.contrib import admin
# from django.urls import path, include
#
# from rest_framework_nested.routers import (
#     DefaultRouter,
#     NestedDefaultRouter,
# )
#
from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token

# from apps.job_scripts import urls as job_script_urls
# from apps.job_submission import urls as job_submission_urls
# from apps.application import urls as application_urls
from apps.job_scripts import views as job_scripts_views
from apps.job_submissions import views as job_submission_views
from apps.applications import views as application_views


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('apps.job_scripts.urls')),
    # path('job-scripts/', job_scripts_views.,),
    # path(
    #     'job-submission/',
    #     include(job_submission_urls),
    # ),
    # path(
    #     'application/',
    #     include(application_urls),
    # ),
    path('api-token-auth/', obtain_jwt_token),
]
