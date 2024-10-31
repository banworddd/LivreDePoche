from rest_framework.permissions import BasePermission

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Разрешает доступ к GET-запросам для всех пользователей, а к POST и DELETE только аутентифицированным.
    """

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        return request.user and request.user.is_authenticated