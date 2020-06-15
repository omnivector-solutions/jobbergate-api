from rest_framework import mixins, viewsets, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status

from apps.job_scripts.models import JobScript
from apps.job_scripts.serializers import JobScriptSerializer


class JobScriptListView(generics.ListCreateAPIView):
    """
    list view for 'job-script/'
    """
    queryset = JobScript.objects.all()
    serializer_class = JobScriptSerializer

    def delete(self, request, JobScript_pk, format=None):
        jobscript = JobScript.objects.get(id=JobScript_pk)
        jobscript.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def put(self, request, JobScript_pk, format=None):
    #     jobscript = JobScript.objects.get(pk=JobScript_pk)
    #     data = request.data
    #     serializer = JobScriptSerializer(instance=jobscript, data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)


class JobScriptView(generics.RetrieveUpdateDestroyAPIView):
    '''
    detail view for 'job-script/<int:pk>'
    '''
    serializer_class = JobScriptSerializer
    queryset = JobScript.objects.all()