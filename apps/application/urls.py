from django.urls import path, include

from apps.application import views


urlpatterns = [
    # ApplicationListOrCreateView will return a list of all of the objects on GET
    # and allow the creation of a job-script on POST.
    #
    # /job-scripts GET - Returns the list of job-scripts.
    #              POST - Allows to create a job-script.
    #
    path(
        '',
        views.ApplicationListOrCreateView.as_view(),
    ),

    # ApplicationDetailView lets you perform CRUD operations on the 
    # the object.
    #
    # /job-scripts/<pk>/ GET - Get details about a single job-script.
    #                    UPDATE - Update details about a job-script.
    #                    DELETE - Delete a job-script.
    #                      
    path(
        '<int:pk>/',
        views.ApplicationDetailView.as_view()
    ),
]
