# jobbergate urls
from django.contrib import admin
from django.urls import include
from django.conf.urls import url
from jobbergate import views
from django.urls import include, path
# from rest_framework import routers
#
# router = routers.DefaultRouter()
# router.register(r'ApplicationListView', views.ApplicationListView)

urlpatterns = [
    path('ApplicationListView/', views.ApplicationListView),
    path('ApplicationCreateView/', views.ApplicationCreateView),
    path('JobListView/', views.JobListView),
    path('JobCreateView/', views.JobCreateView),
    path('JobDetailView/', views.JobDetailView),
    path('JobQueueListView/', views.JobQueueListView),
    path('JobQueueDetailView/', views.JobQueueDetailView),
]
