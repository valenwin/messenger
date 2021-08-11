from rest_framework import serializers

from ...accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["id"]
        read_only_fields = ["id"]
