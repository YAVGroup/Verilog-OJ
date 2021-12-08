from rest_framework import permissions
from submission.models import Submission


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
            # return True

        # Write permissions are only allowed to the owner of the snippet.
        # return obj.owner == request.user

        if obj.name == "code.v":
            sub = Submission.objects.filter(submit_files=obj)
            if sub[0].user == request.user :
                return True
            else:
                return False
        elif obj.name == "code_ref.v":
            return False
        else:
            return True
