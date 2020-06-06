from django.urls import path, include

from apps.job_submissions import views


urlpatterns = [
    path(
        '',
        views.JobSubmissionListView.as_view(),
    ),
    path(
        '<int:pk>/',
        views.JobSubmissionDetailView.as_view()
    ),
]
