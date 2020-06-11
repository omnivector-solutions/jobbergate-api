from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from jobbergate.models import Post
from jobbergate.serializers import PostSerializer


# def home(request):
#     tmpl_vars = {'form': PostForm()}
#     return render(request, 'jobbergate/index.html', tmpl_vars)


@api_view(['GET'])
def ApplicationListView(request):
    test_response = ["Application1", "Application2", "Application3"]
    return Response(test_response)


@api_view(['GET', 'POST'])
def ApplicationCreateView(request):
    test_response = "Application Created"
    return Response(test_response)

@api_view(['GET'])
def JobListView(request):
    test_response = ["Application1", "Application2", "Application3"]
    return Response(test_response)

@api_view(['POST'])
def JobCreateView(request):
    test_response = "Job Created"
    return Response(test_response)

@api_view(['GET', 'POST'])
def JobDetailView(request):
    test_response = ["Job1", "Job2", "Job3"]
    return Response(test_response)

@api_view(['GET'])
def JobQueueListView(request):
    test_response = ["Job1", "Job2", "Job3"]
    return Response(test_response)

@api_view(['GET', 'POST'])
def JobQueueDetailView(request):
    test_response = ["Job1", "Job2", "Job3"]
    return Response(test_response)

