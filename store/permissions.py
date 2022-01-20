from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """Класс, для определения, что запрос выполняет владелец книги"""

    # has_object_permission потому, что делаем с конкретным объектом - книгой
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and (obj.owner == request.user or
                                               request.user.is_staff)
        )