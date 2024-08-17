from rest_framework import serializers
from .models import Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('id', 'image_name', 'image_file', 'uploaded_at', 'image_duration')
