from django.urls import path

from apps.job_scripts import views


urlpatterns = [
    path('job-script/', views.JobScriptListView.as_view()),
    path('job-script/<int:pk>/', views.JobScriptView.as_view())
]
