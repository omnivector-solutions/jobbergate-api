import ast
import io
import tempfile
import json

from django.http import FileResponse, HttpResponse
from wsgiref.util import FileWrapper
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from jobbergate_api.settings import S3_BUCKET
from jinja2 import Template
from zipfile import ZipFile

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
    client = boto3.client('s3')

    def post(self, request, format=None):
        data = request.data
        parser_class = (FileUploadParser,)
        if 'upload_file' not in request.data:
            raise ParseError("Empty content")
        param_file = data['upload_file'].read()
        dict_str = param_file.decode("UTF-8")
        param_dict = ast.literal_eval(dict_str)
        application_id = data['application']

        application = Application.objects.get(id=application_id)
        obj = self.client.get_object(
            Bucket=S3_BUCKET,
            Key=application.application_location

        )
        buf = io.BytesIO(obj['Body'].read())
        tar = tarfile.open(fileobj=buf)
        print(param_dict['supporting_files'])
        template_files = {}

        # existing functionality to render the job script
        # this is what is returned in the job_script_data_as_str field
        for member in tar.getmembers():
            if member.name == param_dict['default_template']:
                contentfobj = tar.extractfile(member)
                template_files["application.sh"] = contentfobj.read().decode("utf-8")
            if member.name in param_dict['supporting_files']:
                contentfobj = tar.extractfile(member)
                filename = param_dict['supporting_files_output_name'][member.name]
                print(f"filename is {filename}")
                template_files[filename] = contentfobj.read().decode("utf-8")
                # template_file += "\nNEW_FILE\n"
                # template_file += contentfobj.read().decode("utf-8")
        # in progress functionality to render all supporting files and
        # return them as a tar with the response

        # #try zip
        # in_memory = io.BytesIO()
        # zf = ZipFile(in_memory, mode="w")
        #
        # # If you have data in text format that you want to save into the zip as a file
        # for member in tar.getmembers():
        #     if member.name in param_dict['supporting_files']:
        #         print(f"file is {member.name}")
        #         contentfobj = tar.extractfile(member)
        #         supporting_file = contentfobj.read().decode("utf-8")
        #         # template = Environment(loader=BaseLoader).from_string(supporting_file)
        #         template = Template(supporting_file)
        #         rendered_str = template.render(data=param_dict)
        #         zf.writestr(member.name, rendered_str)
        #
        # # Close the zip file
        # # zf.close()
        #
        # # Go to beginning
        # in_memory.seek(0)

        # read the data

        # try:
        #     zip_response = FileResponse(open(zf, 'rb'))
        # except:
        #     print("failed on FileResponse(open(zf, 'rb'))")

        # rendered_tar.close()
        # print("filename")
        # zf.filename = "test.zip"
        # print(zf.filename)
        #
        # # generate the file
        # file = open(zf, 'rb')
        # zio_response = HttpResponse(FileWrapper(file), content_type='application/zip')
        # zip_response['Content-Disposition'] = f"attachment; filename={zf.filename}"

        # create tar file where rendered supporting files will be added
        # tmp_file = io.BytesIO(bytearray())
        # rendered_tar = tarfile.open(fileobj=tmp_file)

        with tempfile.NamedTemporaryFile('wb', suffix='.tar.gz', delete=False) as f:
            with tarfile.open(fileobj=f, mode='w:gz') as rendered_tar:
                for member in tar.getmembers():
                    if member.name in param_dict['supporting_files']:
                        print(f"file is {member.name}")
                        contentfobj = tar.extractfile(member)
                        supporting_file = contentfobj.read().decode("utf-8")
                        # template = Environment(loader=BaseLoader).from_string(supporting_file)
                        template = Template(supporting_file)
                        rendered_str = template.render(data=param_dict)
                        tarinfo = tarfile.TarInfo(member.name)
                        # rendered_file = io.StringIO(rendered_str)
                        # rendered_file.write(rendered_str)
                        # rendered_file.close()
                        rendered_tar.addfile(tarinfo, io.StringIO(rendered_str))
            f.flush()
            f.seek(0)


        tar_response = FileResponse(rendered_tar)


        # tar_response = HttpResponse(content_type='application/x-gzip')
        # tar_response['Content-Disposition'] = f'attachment; filename={rendered_tar.name}'

        for key, value in template_files.items():
            template = Template(value)
            # TODO Identify this file not hard code once working
            rendered_js = template.render(data=param_dict)
            template_files[key] = rendered_js


        data['job_script_data_as_string'] = json.dumps(template_files)
        print(data['job_script_data_as_string'])

        serializer = JobScriptSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            # return tar_response
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