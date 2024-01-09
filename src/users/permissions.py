from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(obj.owner)
        print(obj.captain)
        print(request.user)
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user or obj.captain == request.user
