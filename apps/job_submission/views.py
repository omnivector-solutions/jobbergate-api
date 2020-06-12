from rest_framework import permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from apps.job_submission.models import JobSubmission
from apps.job_submission.serializers import JobSubmissionSerializer


class JobSubmissionListOrCreateView(APIView):
    """
    JobSubmissionListOrCreateView will return a list of all of the objects on GET
    and allow the creation of a job-script on POST.
    
    /job-submission GET - Returns the list of job-submission.
                 POST - Allows to create a job-script.
    """

    # permission_classes = [permissions.IsAuthenticated]
    # serializer_class = JobSubmissionSerializer
    # queryset = JobSubmission.objects.all()
    def get_object(self, pk):
        try:
            return JobSubmission.objects.get(pk=pk)
        except JobSubmission.DoesNotExist:
            raise Http404

    def get(self, request):
        user = self.request.user
        print(user)
        job_submission = JobSubmission.objects.get(job_submission_owner=user)
        serializer = JobSubmissionSerializer(data=job_submission, many=True)

        print(serializer.__dict__)
        return Response(JSONRenderer().render(serializer.data))
        # pass

    def post(self, request, format=None):
        serializer = JobSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     user = self.request.user
    #     job_submission = JobSubmission.objects.get(job_submission_owner=user)
    #     serializer = JobSubmissionSerializer(data=job_submission, many=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # pass


class JobSubmissionDetailView(APIView):
    """Job script get, post, update, delete operations.

    * Requires token authentication.

    endpoint: job-submission/<pk>/
    """

    def get(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
