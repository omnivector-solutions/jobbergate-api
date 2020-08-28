import uuid
import tarfile
import io
import yaml

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

        application_file = tar_extract.extractfile("jobbergate.py")
        data['application_file'] = application_file.read()

        # application_config = tar_extract.extractfile("jobbergate.yaml")
        # data['application_config'] = application_config.read()
        application_config = tar_extract.extractfile("jobbergate.yaml").read()
        application_config = yaml.load(application_config)
        templates = []
        for member in tar_extract.getmembers():
            if ".j2" in member.name:
                templates.append(member.name)


        application_config['jobbergate_config']['template_files'] = templates
        data['application_config'] = yaml.dump(application_config)

        application_uuid = str(uuid.uuid4())
        user_id = data['application_owner']

        s3_key = f"jobbergate-resources/{user_id}/{application_uuid}/jobbergate.tar.gz"
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


    def put(self, request, pk, format=None):
        application = Application.objects.get(id=pk)

        data = request.data
        serializer = ApplicationSerializer(instance=application, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
