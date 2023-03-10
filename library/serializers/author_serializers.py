from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from library.models import Author


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        exclude = ['id', 'created_at', 'updated_at']
