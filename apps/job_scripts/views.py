import copy
import io
import json
import tarfile
import tempfile

import boto3
from jinja2 import Template
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from apps.applications.models import Application
from apps.job_scripts.models import JobScript
from apps.job_scripts.serializers import JobScriptSerializer
from jobbergate_api.settings import S3_BUCKET


# from rest_framework.parsers import FileUploadParser  # FIXME - why was this here?


class CustomDjangoModelPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)  # from EunChong's answer
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]


class JobScriptListView(generics.ListCreateAPIView):
    """
    list view for 'job-script/'
    """

    queryset = JobScript.objects.all()
    serializer_class = JobScriptSerializer
    permission_classes = [CustomDjangoModelPermission]
    client = boto3.client("s3")

    def post(self, request, format=None):
        data = request.data
        # parser_class = (FileUploadParser,)  # FIXME - why was this here?
        if "upload_file" not in request.data:
            raise ParseError("Empty content")
        param_file = data["upload_file"].read()
        dict_str = param_file.decode("UTF-8")
        # param_dict = ast.literal_eval(dict_str)
        param_dict = json.loads(dict_str)
        param_dict_flat = {}
        for key, value in param_dict.items():
            for nest_key, nest_value in param_dict[key].items():
                param_dict_flat[nest_key] = nest_value
        application_id = data["application"]

        application = Application.objects.get(id=application_id)
        obj = self.client.get_object(
            Bucket=S3_BUCKET, Key=application.application_location
        )
        buf = io.BytesIO(obj["Body"].read())
        tar = tarfile.open(fileobj=buf)
        template_files = {}
        try:
            support_files_ouput = param_dict_flat["supporting_files_output_name"]
        except KeyError:
            support_files_ouput = []

        try:
            supporting_files = param_dict_flat["supporting_files"]
        except KeyError:
            supporting_files = []

        # This is to handle filename OR full path in tar file
        default_template = [
            param_dict_flat["default_template"],
            "templates/" + param_dict_flat["default_template"],
        ]
        for member in tar.getmembers():
            if member.name in default_template:
                contentfobj = tar.extractfile(member)
                template_files["application.sh"] = contentfobj.read().decode("utf-8")
            if member.name in supporting_files:
                match = [x for x in support_files_ouput if member.name in x]
                contentfobj = tar.extractfile(member)
                filename = support_files_ouput[match[0]][0]
                template_files[filename] = contentfobj.read().decode("utf-8")

        # Use tempfile to generate .tar in memory - NOT write to disk
        with tempfile.NamedTemporaryFile("wb", suffix=".tar.gz", delete=False) as f:
            with tarfile.open(fileobj=f, mode="w:gz") as rendered_tar:
                for member in tar.getmembers():
                    if member.name in supporting_files:
                        contentfobj = tar.extractfile(member)
                        supporting_file = contentfobj.read().decode("utf-8")
                        template = Template(supporting_file)
                        rendered_str = template.render(data=param_dict_flat)
                        tarinfo = tarfile.TarInfo(member.name)
                        rendered_tar.addfile(tarinfo, io.StringIO(rendered_str))
            f.flush()
            f.seek(0)

        job_script_data_as_string = ""
        for key, value in template_files.items():
            template = Template(value)
            # TODO Identify this file not hard code once working
            rendered_js = template.render(data=param_dict_flat)
            job_script_data_as_string
            template_files[key] = rendered_js

        data["job_script_data_as_string"] = json.dumps(template_files)

        serializer = JobScriptSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, JobScript_pk, format=None):
        jobscript = JobScript.objects.get(id=JobScript_pk)
        jobscript.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobScriptView(generics.RetrieveUpdateDestroyAPIView):
    """
    detail view for 'job-script/<int:pk>'
    """

    serializer_class = JobScriptSerializer
    permission_classes = [CustomDjangoModelPermission]
    queryset = JobScript.objects.all()

    def put(self, request, pk, format=None):
        jobscript = JobScript.objects.get(id=pk)
        data = request.data
        serializer = JobScriptSerializer(instance=jobscript, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
