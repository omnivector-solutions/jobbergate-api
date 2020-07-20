import os
import json
import ast
import io

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from jinja2 import Template

import boto3
import tarfile

from apps.applications.models import Application
from apps.job_scripts.models import JobScript
from apps.job_scripts.serializers import JobScriptSerializer


class JobScriptListView(generics.ListCreateAPIView):
    """
    list view for 'job-script/'
    """
    queryset = JobScript.objects.all()
    serializer_class = JobScriptSerializer
    bucket = boto3.resource('s3').Bucket('omnivector-misc')

    def post(self, request, format=None):
        data = request.data
        parser_class = (FileUploadParser,)
        if 'upload_file' not in request.data:
            raise ParseError("Empty content")
        param_file = data['upload_file'].read()
        dict_str = param_file.decode("UTF-8")
        param_dict = ast.literal_eval(dict_str)

        application = Application.objects.get(id=data['application'])
        obj = self.bucket.Object(application.application_location)
        buf = io.BytesIO(obj.get()["Body"].read())  # reads whole gz file into memory
        tar = tarfile.open(fileobj=buf)
        # use "tar" as a regular TarFile object
        for member in tar.getmembers():
            if ".j2" in member.name:
                contentfobj = tar.extractfile(member)
                template_file = contentfobj.read().decode("utf-8")

        template = Template(template_file)

        # TODO Identify this file not hard code once working
        rendered_js = template.render(param_dict=param_dict)
        data['job_script_data_as_string'] = rendered_js

        serializer = JobScriptSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, JobScript_pk, format=None):
        jobscript = JobScript.objects.get(id=JobScript_pk)
        jobscript.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobScriptView(generics.RetrieveUpdateDestroyAPIView):
    '''
    detail view for 'job-script/<int:pk>'
    '''
    serializer_class = JobScriptSerializer
    queryset = JobScript.objects.all()

    def put(self, request, pk, format=None):
        jobscript = JobScript.objects.get(id=pk)
        data = request.data
        serializer = JobScriptSerializer(instance=jobscript, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)