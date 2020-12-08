from django.urls import path

from apps.applications import views


urlpatterns = [
    path("application/", views.ApplicationListView.as_view()),
    path("application/<int:pk>/", views.ApplicationView.as_view()),
]
