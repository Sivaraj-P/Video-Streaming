from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Video
class VideoSerializer(serializers.ModelSerializer):
    created_by=UserSerializer(read_only=True)

    class Meta:
        model=Video
        fields='__all__'