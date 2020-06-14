from django.urls import path, include

from apps.job_submissions import views


urlpatterns = [
    # JobSubmissionListOrCreateView will return a list of all of the objects on GET
    # and allow the creation of a job-submission on POST.
    #
    # /job-submission GET - Returns the list of job-submission.
    #              POST - Allows to create a job-submission.
    #
    path(
        '',
        views.JobSubmissionListOrCreateView.as_view(),
    ),

    # JobSubmissionDetailView lets you perform CRUD operations on the 
    # the object.
    #
    # /job-submission/<pk>/ GET - Get details about a single job-submission.
    #                    UPDATE - Update details about a job-submission.
    #                    DELETE - Delete a job-submission.
    #                      
    path(
        '<int:pk>/',
        views.JobSubmissionDetailView.as_view()
    ),
]
