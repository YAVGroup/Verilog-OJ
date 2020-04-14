from rest_framework.permissions import BasePermission

class GetOnlyPermission(BasePermission):
    """
    普通用户只能GET的权限
    """
    def has_permission(self, request, view):
        if(request.method == 'GET'):
            return True
        else:
            return request.user.is_superuser

class OthersGetOnlyPermission(BasePermission):
    """
    对其他人的信息，普通用户只能GET的权限
    """
    def has_object_permission(self, request, view, obj):
        if(request.method == 'GET'):
            return True
        else:
            return request.user == obj or request.user.is_superuser
