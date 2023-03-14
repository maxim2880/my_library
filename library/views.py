from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from library.models import Author, Book, Reader
from library.serializers.author_serializers import AuthorSerializer
from library.serializers.book_serializers import BookSerializer
from library.serializers.reader_serializers import ReaderSerializer
from .permissions import PermissionPolicyMixin, AdminOrOwnerPermission


class AuthorViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_fields = ['name', 'surname']

    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
        'retrieve': [IsAuthenticated]
    }

    # list, create, update, destroy, retrieve


class BookViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
        'retrieve': [IsAuthenticated]
    }


class ReaderViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'surname', 'phone_number']

    permission_classes_per_method = {
        'list': [AdminOrOwnerPermission],
        'create': [AllowAny],
        'update': [AdminOrOwnerPermission],
        'destroy': [AdminOrOwnerPermission],
        'retrieve': [AdminOrOwnerPermission]
    }

    def perform_destroy(self, instance: Reader):
        instance.is_active = False
        instance.save()
