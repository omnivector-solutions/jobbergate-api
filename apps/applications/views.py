import uuid
import tarfile
import io

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
        tar_extract = tarfile.open(fileobj=data['upload_file'].file)

        # try:
        application_file = tar_extract.extractfile("application.py")
        data['application_file'] = application_file.read()
        # except Exception as e:
        #     print(e)
        #     print("no application.py to add to data")

        application_config = tar_extract.extractfile("jobbergate.yaml")
        data['application_config'] = application_config.read()

        application_uuid = str(uuid.uuid4())
        user_id = data['application_owner']

        s3_key = f"jobbergate-resources/{user_id}/{application_uuid}/application.tar.gz"
        data['application_location'] = s3_key

        serializer = ApplicationSerializer(data=data)

        tar_file.seek(0)
        if serializer.is_valid():
            serializer.save()
            self.client.put_object(
                Body=tar_file,
                Bucket=S3_BUCKET,
                Key=s3_key
            )
            return Response(serializer.data)
        else:
            print(serializer.data)


class ApplicationView(generics.RetrieveUpdateDestroyAPIView):
    '''
    detail view for 'application/<int:pk>'
    '''
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    client = boto3.client('s3')

    # def get(self, request, pk):
    #     application = Application.objects.get(id=pk)
    #     print(type(application.application_location))
    #     print(application.application_location)
    #     obj = self.client.get_object(
    #         Bucket=S3_BUCKET,
    #         Key=application.application_location
    #
    #     )
    #     buf = io.BytesIO(obj['Body'].read())
    #     tar = tarfile.open(fileobj=buf)
    #     application_file = tar.extractfile("application.py").read()
    #     print(type(application_file))
    #
    #     serializer = ApplicationSerializer(instance=application)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        application = Application.objects.get(id=pk)

        data = request.data
        serializer = ApplicationSerializer(instance=application, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)