from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Handle different object types
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'player'):
            return obj.player.user == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False