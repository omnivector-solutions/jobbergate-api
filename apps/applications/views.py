import uuid
import tarfile
import io
import yaml
from io import StringIO

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from jobbergate_api.settings import S3_BUCKET

import boto3

from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer


def get_application(data):
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

    return tar_file, tar_extract, data

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
        if 'upload_file' in request.data:
            tar_file, tar_extract, data = get_application(data)
            serializer = ApplicationSerializer(data=data)

            tar_file.seek(0)
            if serializer.is_valid():
                obj = serializer.save()
                application = Application.objects.get(id=obj.id)
                self.client.put_object(
                    Body=tar_file,
                    Bucket=S3_BUCKET,
                    Key=application.application_location
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
        if 'upload_file' in data:
            tar_file, tar_extract, data = get_application(data)
        else:
            print(data)

        tar_update = tarfile.open(fileobj=data['upload_file'].file, mode="w|gz")
        if data['application_file'] != application.application_file:
            file_change = True
            wr_application_file = io.StringIO()
            wr_application_file.write(data['application_file'])
            wr_application_file.close()
            tar_update.addfile(tarfile.TarInfo("jobbergate.py"), fileobj=wr_application_file)
        else:
            file_change = False

        if data['application_config'] != application.application_config:
            config_change = True
            wr_config_file = io.StringIO()
            wr_config_file.write(data['application_config'])
            wr_config_file.close()
            tar_update.addfile(tarfile.TarInfo("jobbergate.yaml"), fileobj=wr_config_file)
        else:
            config_change = False

        serializer = ApplicationSerializer(instance=application, data=data)

        # tar_file.seek(0)
        if serializer.is_valid():
            serializer.save()
            #if file or config changed then upload to s3 and overwrite at existing s3 key
            if file_change or config_change:
                print(tar_extract.getmembers())
                tar_update.close()
                self.client.put_object(
                    Body=tar_update,
                    Bucket=S3_BUCKET,
                    Key=application.application_location
                )

            return Response(serializer.data)
