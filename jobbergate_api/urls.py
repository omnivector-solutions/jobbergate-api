from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_jwt.views import obtain_jwt_token


schema_view = get_schema_view(
    openapi.Info(
        title="Jobbergate API",
        default_version="v1",
        description="API for Jobbergate-CLI and Jobbergate-WEB",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_urlpatterns = [
    path("accounts/", include("rest_registration.api.urls")),
    # path('', include('links.api.urls')),
]

urlpatterns = [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    url(r"^healthcheck/", include("health_check.urls")),
    path("admin/", admin.site.urls),
    path("", include("apps.job_scripts.urls")),
    path("", include("apps.job_submissions.urls")),
    path("", include("apps.applications.urls")),
    path("api-token-auth/", obtain_jwt_token),
    path("", include(api_urlpatterns)),
]
