# django-rest-framework
+ Tạo 1 API router: GET, POST, PUT, and DELETE
+ Check token tồn tại trong db mysql

## create virtual environment
	```python -m venv venv```
# 👇️ activate on Windows (cmd.exe)
	```venv\Scripts\activate.bat```

## install django: 
	```pip install django```
	
## create a new project
	```django-admin startproject management_api```
	
## run test
	```
	cd management_api
	python manage.py runserver <Tên Cổng>
	```
	
##  create the app
	```python manage.py startapp api```

## migrate your models into the database
	```
	python manage.py makemigrations
	python manage.py migrate	
	```
	
## Hệ thống Admin trong Python Django
	```python manage.py createsuperuser```
	http://localhost:8000/admin/

## Install django-rest-framework
    ```pip install djangorestframework```

## Mã hóa Ms office file
    ```pip install msoffcrypto-tool```

## Install Mysql
    ```pip install mysqlclient```

## Add config to setting
\management_api\management_api\settings.py
    ```
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'api',
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'biz': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'biz',
            'USER': 'root',
            'PASSWORD': '',
            'HOST':'localhost',
            'PORT':'3306',
        }
    }
    ```

## Default router GET, POST, PUT, and DELETE
\management_api\api\urls.py
    ```
    from django.urls import path

    from .views import (
        TodoListApiView,
        TodoListApi2View,
    )
    urlpatterns = [
        path('api', TodoListApiView.as_view()),
        path('api2', TodoListApi2View.as_view()),
    ]
    ```

\management_api\api\views.py
    ```
    from django.shortcuts import render
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status
    # from .permissions import IsBizConfigToken
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
    ```
\management_api\management_api\urls.py
    ```
    from django.contrib import admin
    from django.urls import path, include

    from api import urls as api_urls

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api-auth/', include('rest_framework.urls')),
        path('portal/', include(api_urls)),
    ]
    ```

## Add check token
add new file  \management_api\api\permissions.py
    ```
    from rest_framework import permissions
    from django.db import connections

    class IsBizConfigToken(permissions.BasePermission):
        def check_token_from_biz_config(self, request):
            biz_token_key = request.headers.get("X-GI-Authorization")
            if not biz_token_key:
                return False
            
            with connections['biz'].cursor() as cursor:
                cursor.execute("SELECT * FROM configure WHERE `key`='portal_token_api' AND value = %s", [biz_token_key])
                row = cursor.fetchone()
                print(row)
                if not row:
                    return False
                
            return True

        def has_permission(self, request, view):
            isbizconfigtoken = self.check_token_from_biz_config(request)
            if isbizconfigtoken:
                return True
            
            return False

    ```
update code \management_api\api\views.py
    ```
    from .permissions import IsBizConfigToken

    permission_classes = [IsBizConfigToken]
    ```

check database:
```SELECT * FROM biz.configure where `key` = 'portal_token_api' and `value` = 'c7ab02cd28aa60c142fedb489f9fe3ee716c6993eb9330de626f12defb3bc6f5';```

check postman:
    ```
    http://127.0.0.1:8000/portal/api
    X-GI-Authorization: c7ab02cd28aa60c142fedb489f9fe3ee716c6993eb9330de626f12defb3bc6f5
    ```

## Read file excel with password
