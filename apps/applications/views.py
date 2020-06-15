from rest_framework import mixins, viewsets, permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer


class ApplicationListView(generics.ListCreateAPIView):
    """
    list view for 'application/'
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def delete(self, request, Application_pk, format=None):
        application = Application.objects.get(id=Application_pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationView(generics.RetrieveUpdateDestroyAPIView):
    '''
    detail view for 'application/<int:pk>'
    '''
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()