from django.contrib import admin
from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.job_scripts.urls')),
    path('', include('apps.job_submission.urls')),
    path('', include('apps.application.urls')),
    path('api-token-auth/', obtain_jwt_token),
]
