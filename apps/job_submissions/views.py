import copy

from rest_framework import generics, status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from apps.job_submissions.models import JobSubmission
from apps.job_submissions.serializers import JobSubmissionSerializer


class CustomDjangoModelPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)  # from EunChong's answer
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]


class JobSubmissionListView(generics.ListCreateAPIView):
    """
    list view for 'job-submission/'
    """

    queryset = JobSubmission.objects.all()
    serializer_class = JobSubmissionSerializer
    permission_classes = [CustomDjangoModelPermission]

    def delete(self, request, JobSubmission_pk, format=None):
        jobscript = JobSubmission.objects.get(id=JobSubmission_pk)
        jobscript.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobSubmissionView(generics.RetrieveUpdateDestroyAPIView):
    """
    detail view for 'job-submission/<int:pk>'
    """

    serializer_class = JobSubmissionSerializer
    permission_classes = [CustomDjangoModelPermission]
    queryset = JobSubmission.objects.all()

    def put(self, request, pk, format=None):
        jobsubmission = JobSubmission.objects.get(id=pk)
        data = request.data
        serializer = JobSubmissionSerializer(instance=jobsubmission, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
