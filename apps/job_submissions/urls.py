from django.urls import path

from apps.job_submissions import views


urlpatterns = [
    path("job-submission/", views.JobSubmissionListView.as_view()),
    path("job-submission/<int:pk>/", views.JobSubmissionView.as_view()),
]
