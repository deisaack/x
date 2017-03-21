from django.conf.urls import url

from .views import (
    all_books,
    register_new_book,
    register_new_category,
    register_new_publisher,
    borrow_book,
    book_detail,
    book_delete,
    book_update,
    book_list,
    )

urlpatterns = [
    url(r'^all/$', all_books, name='all'),
    url(r'^$', book_list, name='list'),
    url(r'^add-book/$', register_new_book, name='add-book'),
    url(r'^add-category/$', register_new_category, name='add-category'),
    url(r'^add-publisher/$', register_new_publisher, name='add-publisher'),
    url(r'^(?P<slug>[\w-]+)/$', book_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', book_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/borrow/$', borrow_book, name='borrow'),
    url(r'^(?P<slug>[\w-]+)/delete/$', book_delete),

]
