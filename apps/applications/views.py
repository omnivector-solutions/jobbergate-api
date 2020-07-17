import os

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

import boto3

from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer


class ApplicationListView(generics.ListCreateAPIView):
    """
    list view for 'application/'
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    bucket = boto3.resource('s3').Bucket('omnivector-misc')

    def delete(self, request, Application_pk, format=None):
        application = Application.objects.get(id=Application_pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        data = request.data
        parser_class = (FileUploadParser,)
        if 'upload_file' not in request.data:
            raise ParseError("Empty content")
        tar_file = data['upload_file']

        filename = data['application_location'].split("/")[-1]

        path = default_storage.save(filename, ContentFile(tar_file.read()))
        self.bucket.upload_file(
            os.path.join(settings.MEDIA_ROOT, path),
            data['application_location'])

        serializer = ApplicationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class ApplicationView(generics.RetrieveUpdateDestroyAPIView):
    '''
    detail view for 'application/<int:pk>'
    '''
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()

    def put(self, request, pk, format=None):
        application = Application.objects.get(id=pk)

        data = request.data
        serializer = ApplicationSerializer(instance=application, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)