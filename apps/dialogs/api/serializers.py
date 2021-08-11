from django.db import transaction
from rest_framework import serializers

from ..models import Thread, Message
from ...accounts.api.serializers import UserSerializer
from ...accounts.models import User


class MessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    sender = UserSerializer(read_only=True)
    is_read = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = Message
        fields = ["id", "text", "sender", "is_read", "created_at", "updated_at"]
        read_only_fields = ["id"]


class ThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    last_message = serializers.SerializerMethodField()
    unread_messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ["id", "participants", "unread_messages_count", "last_message"]
        read_only_fields = ["id"]

    def get_last_message(self, obj):
        try:
            post = obj.thread_messages.latest("created_at")
            serializer = MessageSerializer(post)
            return serializer.data
        except Message.DoesNotExist:
            return None

    def get_unread_messages_count(self, obj):
        return obj.thread_messages.exclude(is_read=True).count()

    def validate_participants(self, value):
        for participant in value:
            if not User.objects.filter(pk=participant["id"]).exists():
                raise serializers.ValidationError("User not exists.")
        return value

    def create(self, validated_data):
        participants = validated_data.pop("participants", [])

        with transaction.atomic():
            thread = super().create(validated_data)
            for participant in participants[:2]:
                thread.participants.add(participant["id"])

        return thread

    def update(self, instance, validated_data):
        participants = validated_data.pop("participants", [])
        instance.participants.set([])

        with transaction.atomic():
            thread = super().update(instance, validated_data)

            for participant in participants[:2]:
                thread.participants.add(participant["id"])

        return thread
