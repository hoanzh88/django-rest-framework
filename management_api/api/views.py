from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsBizConfigToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TodoListApiView(APIView):
    # permission_classes = [IsBizConfigToken]
    def get(self, request, *args, **kwargs):
        return Response("GET method", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'method':  request.method,
            'user-agent': request.headers.get("User-Agent"),
            'status': status.HTTP_200_OK
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, *args, **kwargs):
        return Response("PUT method", status=status.HTTP_200_OK)
    
    def delete(self, *args, **kwargs):
        return Response("DELETE method", status=status.HTTP_200_OK)
    
class TodoListApi2View(APIView):
    def get(self, request, *args, **kwargs):
        return Response("GET method - 2", status=status.HTTP_200_OK)