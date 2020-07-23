from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from jobbergate_api.settings import S3_BUCKET

import boto3

from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer


class ApplicationListView(generics.ListCreateAPIView):
    """
    list view for 'application/'
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    client = boto3.client('s3')
    #TODO once working - populate dynamic

    def delete(self, request, pk, format=None):
        application = Application.objects.get(id=pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        data = request.data
        parser_class = (FileUploadParser,)
        if 'upload_file' not in request.data:
            raise ParseError("Empty content")
        tar_file = data['upload_file']

        serializer = ApplicationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            user_id = serializer.data['application_owner']
            application_id = serializer.data['id']
            application_name = serializer.data['application_name']
            print(f"data 1: {serializer.data}")

            self.client.put_object(
                Body=tar_file,
                Bucket=S3_BUCKET,
                Key=(
                    "jobbergate-resources/"
                    f"{user_id}/"
                    f"{application_name}/"
                    f"{application_id}/"
                    "application.tar.gz"
                )
            )
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