from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsBizConfigToken
from rest_framework.permissions import IsAuthenticated
import msoffcrypto
import io
import os
from django.conf import settings
import pandas as pd
from django.core.files import File
# Create your views here.
class TodoListApiView(APIView):
    # permission_classes = [IsBizConfigToken]

    def get(self, request, *args, **kwargs):
        return Response("GET method", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # create the folder if it doesn't exist.
        upload_folder = settings.UPLOAD_EXCEL_PATH
        dir_upload_folder = os.path.join(settings.MEDIA_ROOT, upload_folder)
        os.makedirs(dir_upload_folder, exist_ok=True)

        full_upload_filename = os.path.join(settings.MEDIA_ROOT, upload_folder, request.FILES["file"].name)
        self.handle_uploaded_file(request.FILES["file"], full_upload_filename)
        
        password = request.data.get("password")
        decrypted_file = self.decrypt_file(full_upload_filename, password)
        df = pd.read_excel(decrypted_file)
        data = df.to_json()

        # remove the uploaded file
        os.remove(full_upload_filename)
        return Response(data, status=status.HTTP_200_OK)
    
        # data = {
        #     'method':  request.method,
        #     'user-agent': request.headers.get("User-Agent"),
        #     'datas': df.to_json(),
        #     'status': status.HTTP_200_OK
        # }
        # return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    def save_uploaded_file(path,f):
        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def put(self, *args, **kwargs):
        return Response("PUT method", status=status.HTTP_200_OK)
    
    def delete(self, *args, **kwargs):
        return Response("DELETE method", status=status.HTTP_200_OK)
    
    def decrypt_file(self, file_path, password):
        with open(file_path, "rb") as f:
            file = msoffcrypto.OfficeFile(f)
            file.load_key(password=password)
            decrypted_file = io.BytesIO()
            file.decrypt(decrypted_file)
            decrypted_file.seek(0)
            return decrypted_file
        
    def handle_uploaded_file(self, f, full_filename):
        with open(full_filename, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)

class TodoListApi2View(APIView):
    def get(self, request, *args, **kwargs):
        return Response("GET method - 2", status=status.HTTP_200_OK)