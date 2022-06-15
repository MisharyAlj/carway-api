from rest_framework import permissions


# If the request is a safe method (GET, HEAD, OPTIONS), then allow it. Otherwise, only allow it if the
# user is a superuser
class IsSuperuserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        is_superuser = request.user and request.user.is_superuser
        return is_superuser
