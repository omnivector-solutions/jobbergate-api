from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.job_scripts.urls')),
    path('', include('apps.job_submission.urls')),
    path('', include('apps.application.urls')),
]