from django.contrib import admin

from .models import Book, Category, Publisher, Student


class BookModelAdmin(admin.ModelAdmin):
    list_display = ["title", "no", "borrower"]
    list_display_links = ["no"]
    list_editable = ["title"]
    list_filter = ["borrower", "no"]

    search_fields = ["title", "description"]
    class Meta:
        model = Book


admin.site.register(Book, BookModelAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    model = Category
    class Meta:
       model = Category

admin.site.register(Category, CategoryAdmin)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    class Meta:
        model = Publisher

admin.site.register(Publisher, PublisherAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ['reg_no', 'first_name']
    class Meta:
        model = Student

admin.site.register(Student, StudentAdmin)