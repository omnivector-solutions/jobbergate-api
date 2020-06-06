from django.urls import path, include

from apps.registries import views


urlpatterns = [
    path(
        '',
        views.RegistryListView.as_view(),
    ),
    path(
        '<int:pk>/',
        views.RegistryDetailView.as_view()
    ),
]
