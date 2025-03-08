
from rest_framework.permissions import BasePermission
from .permissions import UserRoles

class UserRoles:
    ADMIN = 'admin'
    WRITER = 'writer'
    READER = 'reader'

    @staticmethod
    def is_admin(user):
        return user.groups.filter(name=UserRoles.ADMIN).exists()

    @staticmethod
    def is_writer(user):
        return user.groups.filter(name=UserRoles.WRITER).exists()

    @staticmethod
    def is_reader(user):
        return user.groups.filter(name=UserRoles.READER).exists()


class IsAdmin(BasePermission):
    """
    Permite apenas administradores.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and UserRoles.is_admin(request.user)

class IsWriter(BasePermission):
    """
    Permite apenas escritores (pode realizar CRUD de notícias).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and UserRoles.is_writer(request.user)

class IsReader(BasePermission):
    """
    Permite apenas leitores (somente leitura das notícias).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and UserRoles.is_reader(request.user)
