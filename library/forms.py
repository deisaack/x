from django import forms


from .models import Book, Category, Publisher


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "no",
            "draft",
        ]

class RegisterBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "publish",
            'publisher',
            'draft',
            'no',
            'category',
            'description',
        ]

class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "image",
            "description",
        ]

class BookPublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = [
            "name",
            "post_address",
            "email",
            'phone',
        ]

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'borrowed',
            'borrower',
        ]

