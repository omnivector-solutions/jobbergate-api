import copy
import io
import os
import tarfile

from rest_framework import generics, status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
import yaml

from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer
from jobbergate_api.botolib import make_s3_client
from jobbergate_api.settings import APPLICATION_FILE, CONFIG_FILE, S3_BUCKET, TAR_NAME


# from rest_framework.parsers import FileUploadParser  # FIXME - why was this here?


TEMP_DIR = "/tmp/jobbergate"


class CustomDjangoModelPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)  # from EunChong's answer
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]


def get_application(data):
    tar_file = data["upload_file"]
    tar_extract = tarfile.open(fileobj=data["upload_file"].file)

    application_file = tar_extract.extractfile("jobbergate.py")
    data["application_file"] = application_file.read()

    application_config = tar_extract.extractfile("jobbergate.yaml").read()
    application_config = yaml.safe_load(application_config)
    templates = []
    for member in tar_extract.getmembers():
        if "templates" in member.name:
            # Means it is in the /templates dir within tarfile
            templates.append(member.name)

    application_config["jobbergate_config"]["template_files"] = templates
    data["application_config"] = yaml.dump(application_config)

    return tar_file, tar_extract, data


def tardir(path, tar_name) -> tarfile.TarFile:
    """
    Create a tar file for the contents of the directory at ``path''

    Returns the closed TarFile after writing the contents
    """
    archive = tarfile.open(tar_name, "w|gz")
    archive.add(path, recursive=True, filter=root_fix)
    archive.close()
    return archive


def root_fix(tarinfo):
    """
    Clean the root of the tarinfo to remove the tempdir prefix
    """
    temp_dir = TEMP_DIR.lstrip("/")
    assert tarinfo.name.startswith(temp_dir), f"data to tar up can only be in {TEMP_DIR} (was /{tarinfo.name})"
    temp_dir_length = len(TEMP_DIR)
    tarinfo.name = tarinfo.name[temp_dir_length:]
    return tarinfo


class ApplicationListView(generics.ListCreateAPIView):
    """
    list view for 'application/'
    """

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [CustomDjangoModelPermission]
    client = make_s3_client(S3_BUCKET)

    def put(self, request, format=None):
        """
        Endpoint for "update application" when using identifier
        """
        application_identifier = request.query_params.get("identifier")
        if application_identifier:
            application = Application.objects.filter(application_identifier=application_identifier).first()
            if not application:
                return Response("Application not found", 404)
        obj = self.client.get_object(Bucket=S3_BUCKET, Key=application.application_location)
        buf = io.BytesIO(obj["Body"].read())
        tar_extract = tarfile.open(fileobj=buf)

        # extract all to /tmp/jobbergate and will overwite if changes
        try:
            os.mkdir(TEMP_DIR)
        except FileExistsError:
            pass
        tar_extract.extractall(path=TEMP_DIR)

        data = request.data

        if data["application_file"] != application.application_file:
            file_change = True
        else:
            file_change = False
        # write over /tmp/jobbergate/jobbergate.py
        os.remove(APPLICATION_FILE)
        wr_application_file = open(APPLICATION_FILE, "w")
        wr_application_file.write(data["application_file"])
        wr_application_file.close()

        if data["application_config"] != application.application_config:
            config_change = True
        else:
            # This is for if ONLY _file is updated because the
            # data submitted wont have ['application_config']
            config_change = False

        # write over /tmp/jobbergate/jobbergate.yaml
        os.remove(CONFIG_FILE)
        wr_config_file = open(CONFIG_FILE, "w")
        wr_config_file.write(data["application_config"])
        wr_config_file.close()

        serializer = ApplicationSerializer(instance=application, data=data)

        if serializer.is_valid():
            serializer.save()
            # if file or config changed then upload to s3 and overwrite at existing s3 key
            if file_change or config_change:
                # dir to tar now has new jobbergate .py and .yaml
                tardir(path=TEMP_DIR, tar_name=TAR_NAME)
                self.client.put_object(
                    Body=open(TAR_NAME, "rb"),
                    Bucket=S3_BUCKET,
                    Key=application.application_location,
                )

            return Response(serializer.data)

    def list(self, request):
        application_identifier = request.query_params.get("identifier")
        if application_identifier:
            application = Application.objects.filter(application_identifier=application_identifier).first()
            if not application:
                return Response("Application not found", 404)
            return Response(ApplicationSerializer(application).data, 200)
        else:
            queryset = self.get_queryset()
            serializer = ApplicationSerializer(queryset, many=True)
            return Response(serializer.data)

    def delete(self, request, pk=None, format=None):
        application_identifier = request.query_params.get("identifier")
        if application_identifier:
            application = Application.objects.filter(application_identifier=application_identifier).first()
            if not application:
                return Response("Application not found", 404)
        else:
            application = Application.objects.filter(id=pk).first()
            if not application:
                return Response("Application not found", 404)

        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        """
        Endpoint for "create application"
        """
        data = request.data
        if Application.objects.filter(application_identifier=data.get("application_identifier")):
            return Response("application_idenfier already exists", 409)
        if "upload_file" in request.data:
            tar_file, tar_extract, data = get_application(data)
            serializer = ApplicationSerializer(data=data)

            tar_file.seek(0)
            if serializer.is_valid():
                obj = serializer.save()
                application = Application.objects.get(id=obj.id)
                self.client.put_object(
                    Body=tar_file,
                    Bucket=S3_BUCKET,
                    Key=application.application_location,
                )
                return Response(serializer.data)
            else:
                print(serializer.data)


class ApplicationView(generics.RetrieveUpdateDestroyAPIView):
    """
    detail view for 'application/<int:pk>'
    """

    serializer_class = ApplicationSerializer
    permission_classes = [CustomDjangoModelPermission]
    queryset = Application.objects.all()
    client = make_s3_client(S3_BUCKET)

    def put(self, request, pk=None, format=None):
        """
        Endpoint for "update application"
        """
        application = Application.objects.filter(id=pk).first()
        if not application:
            return Response("Application not found", 404)
        obj = self.client.get_object(Bucket=S3_BUCKET, Key=application.application_location)
        buf = io.BytesIO(obj["Body"].read())
        tar_extract = tarfile.open(fileobj=buf)

        # extract all to /tmp/jobbergate and will overwite if changes
        try:
            os.mkdir(TEMP_DIR)
        except FileExistsError:
            pass
        tar_extract.extractall(path=TEMP_DIR)

        data = request.data

        if data["application_file"] != application.application_file:
            file_change = True
        else:
            file_change = False
        # write over /tmp/jobbergate/jobbergate.py
        os.remove(APPLICATION_FILE)
        wr_application_file = open(APPLICATION_FILE, "w")
        wr_application_file.write(data["application_file"])
        wr_application_file.close()

        if data["application_config"] != application.application_config:
            config_change = True
        else:
            # This is for if ONLY _file is updated because the
            # data submitted wont have ['application_config']
            config_change = False

        # write over /tmp/jobbergate/jobbergate.yaml
        os.remove(CONFIG_FILE)
        wr_config_file = open(CONFIG_FILE, "w")
        wr_config_file.write(data["application_config"])
        wr_config_file.close()

        serializer = ApplicationSerializer(instance=application, data=data)

        if serializer.is_valid():
            serializer.save()
            # if file or config changed then upload to s3 and overwrite at existing s3 key
            if file_change or config_change:
                # dir to tar now has new jobbergate .py and .yaml
                tardir(path=TEMP_DIR, tar_name=TAR_NAME)
                self.client.put_object(
                    Body=open(TAR_NAME, "rb"),
                    Bucket=S3_BUCKET,
                    Key=application.application_location,
                )

            return Response(serializer.data)
