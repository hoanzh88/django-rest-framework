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
