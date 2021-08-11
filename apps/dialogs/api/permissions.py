from rest_framework import permissions


class IsMessageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, message):
        if (
                request.method in permissions.SAFE_METHODS
                and request.user in message.thread.participants.all()
        ):
            return True
        return message.sender == request.user


class IsSenderThreadParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, message):
        return request.user in message.thread.participants.all()


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, thread):
        return request.user in thread.participants.all()
