from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from library.models import Book, Author
from library.validators import NumbersPageValidator


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='surname')

    num_pages = serializers.IntegerField(validators=[NumbersPageValidator()])

    class Meta:
        model = Book
        exclude = ['created_at', 'updated_at']
        validators = [UniqueTogetherValidator(queryset=Book.objects.all(), fields=['name', 'author'])]
