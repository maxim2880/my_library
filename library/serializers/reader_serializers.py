from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from library.models import Reader, Book
from library.validators import PhoneValidator


class ReaderSerializer(serializers.ModelSerializer):
    books = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field='name', many=True)

    phone_number = serializers.CharField(validators=[PhoneValidator()])

    def validate(self, attrs):
        if len(attrs['books']) > 3:
            raise serializers.ValidationError('Не более 3 книг у читателя на руках')
        return attrs

    def create(self, validated_data):
        if validated_data['books']:
            for book in validated_data['books']:
                if book.num_books == 0:
                    raise serializers.ValidationError('Нет книг невозможно создать пользователя')

        books_data = validated_data.pop('books')
        reader = Reader.objects.create(**validated_data)
        for book_data in books_data:
            book = Book.objects.get(pk=book_data.id)
            if book.num_books > 0:
                book.num_books -= 1
                book.save()
                reader.books.add(book)
            else:
                raise serializers.ValidationError(f"Книги {book.name} нет в наличии")
        return reader

    def update(self, instance, validated_data):
        if validated_data['books']:
            for book in validated_data['books']:
                if book not in instance.books.all():
                    if book.num_books > 0:
                        book.num_books -= 1
                        book.save()
                    else:
                        raise serializers.ValidationError('Книги нет в наличии')
            for book in instance.books.all():
                if book not in validated_data['books']:
                    book.num_books += 1
                    book.save()
            return super().update(instance, validated_data)
        else:
            return super().update(instance, validated_data)

    class Meta:
        model = Reader
        exclude = ['created_at', 'updated_at']
