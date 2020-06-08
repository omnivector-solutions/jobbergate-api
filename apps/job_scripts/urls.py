from django.urls import path, include

from apps.job_scripts import views


urlpatterns = [
    path(
        '',
        views.JobScriptListView.as_view(),
    ),
    path(
        '<int:pk>/',
        views.JobScriptDetailView.as_view()
    ),
]
