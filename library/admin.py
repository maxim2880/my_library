from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode

from library.models import Reader, Book, Author


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'authors_link', 'num_books')
    actions = ['change_num_books']

    @admin.action(description="Убрать книги из библиотеки")
    def change_num_books(self, request, queryset: QuerySet):
        queryset.update(num_books=0)
        self.message_user(request, 'Книги удалены')

    def authors_link(self, obj):
        author = obj.author
        url = reverse("admin:library_author_changelist") + str(author.pk)
        return format_html(f'<a href="{url}"> {author} </a>')

    authors_link.short_description = 'Авторы'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')


class ReaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone_number', 'display_books', 'status')
    list_filter = ('status',)
    search_fields = ('name',)
    actions = ['change_status', 'delete_all_books']

    @admin.action(description="Изменить статус")
    def change_status(self, request, queryset: QuerySet):
        count = queryset.update(status=False)
        self.message_user(request, f'Деактивировано {count} пользователей')

    @admin.action(description='Удалить книги у читателя')
    def delete_all_books(self, request, queryset):
        for book in queryset:
            book.books.clear()
        self.message_user(request, f'Книги удалены')


admin.site.register(Reader, ReaderAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
