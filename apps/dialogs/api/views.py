from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsSenderThreadParticipant, IsMessageOwner, IsParticipant
from ..models import Thread, Message

from .serializers import ThreadSerializer, MessageSerializer
from ...accounts.models import User


class ThreadView(generics.ListCreateAPIView):
    """
    Thread list view
    Create new thread with 2 participants only
    """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class ThreadDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get information about one thread by pk
    Update thread
    Destroy thread and thread's messages while there no participants
    """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsParticipant]

    def get(self, request, *args, **kwargs):
        """
        Get thread and destroy thread and thread's messages while there no participants
        """
        instance = self.get_object()
        instance_participants = self.get_object().participants
        if instance_participants.count() == 0:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return self.retrieve(request, *args, **kwargs)


class MessagesView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsSenderThreadParticipant, IsAuthenticated]

    def get_queryset(self):
        thread = get_object_or_404(Thread, pk=self.kwargs.get("pk"))
        return thread.thread_messages.all()

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        thread = Thread.objects.filter(
            pk=kwargs.get("pk"), participants__id=request.user.id
        ).first()
        if thread is None:
            raise ValidationError("You are not thread participant.")
        sender = get_object_or_404(User, pk=request.user.id)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        serializer.save(sender=sender, thread=thread, text=request.data.get("text"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsMessageOwner]


class MessageReadView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsSenderThreadParticipant]

    def get_queryset(self):
        thread = get_object_or_404(Thread, pk=self.kwargs.get("pk"))
        return thread.thread_messages.all()

    def get(self, request, *args, **kwargs):
        thread = get_object_or_404(Thread, pk=kwargs.get("pk"))
        messages = Message.objects.filter(
            thread=thread, thread__participants__id=request.user.id
        )
        messages.update(is_read=True)
        return Response(data=MessageSerializer(messages, many=True).data)
