from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Проверка, является ли пользователь администратором """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Admins").exists()


class IsTeacher(permissions.BasePermission):
    """ Класс для разрешения доступа только преподавателям """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Teacher").exists()


class IsOwner(permissions.BasePermission):
    """ Класс для разрешения доступа только владельцам """

    def has_object_permission(self, request, view, object):
        if object.owner == request.user:
            return True
        return False
