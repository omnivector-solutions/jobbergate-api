from rest_framework import mixins, viewsets, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from apps.job_scripts.models import JobScript
from apps.job_scripts.serializers import JobScriptSerializer


class JobScriptView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobScriptSerializer
    queryset = JobScript.objects.all()

    def post(self, request):
        return Response({"some": "keyvalue"})


class JobScriptListView(generics.ListCreateAPIView):
    """
    list view for 'job-script/'
    """
    queryset = JobScript.objects.all()
    serializer_class = JobScriptSerializer

class JobScriptView(generics.RetrieveUpdateDestroyAPIView):
    '''
    detail view for 'job-script/<int:pk>'
    '''
    serializer_class = JobScriptSerializer
    queryset = JobScript.objects.all()

