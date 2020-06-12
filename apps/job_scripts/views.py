from rest_framework import mixins, viewsets, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from apps.job_scripts.models import JobScript
from apps.job_scripts.serializers import JobScriptSerializer




class JobScriptView(mixins.ListModelMixin, viewsets.GenericViewSet):
 
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobScriptSerializer
    queryset = JobScript.objects.all()

    def post(self, request):
        return Response({"some": "keyvalue"})


class JobScriptListOrCreateView(APIView):
    """
    JobScriptListOrCreateView will return a list of all of the objects on GET
    and allow the creation of a job-script on POST.
    
    /job-scripts GET - Returns the list of job-scripts.
                 POST - Allows to create a job-script.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobScriptSerializer
    queryset = JobScript.objects.all()

    def get(self, request):
#        user = request.user
#        job_scripts = JobScript.objects.get(user=user)
#        serializer = JobScriptSerializer(data=job_scripts, many=True)
#
#        print(serializer.__dict__)
#        return Response(JSONRenderer().render(serializer.data))
        pass


    def post(self, request):
        pass


class JobScriptDetailView(APIView):
    """Job script get, post, update, delete operations.

    * Requires token authentication.

    endpoint: job-scripts/<pk>/
    """

    def get(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
