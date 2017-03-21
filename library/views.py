try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.urlresolvers import reverse

from .forms import Book, Category, Publisher, BookCategoryForm, BookForm, BookPublisherForm, RegisterBookForm, \
    BorrowBookForm
from .models import Book


def all_books(request):
    today = timezone.now().date()
    queryset_list = Book.objects.active()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Book.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(borower__reg_no__icontains=query) |
            Q(no__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 1000)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    b = Book.objects.all().count()  # .order_by("-timestamp")
    c = Category.objects.all().count()
    p = Publisher.objects.all().count()
    context = {
        "object_list": queryset,
        "title": "Books in Holistic Academy",
        "page_request_var": page_request_var,
        "today": today,
        'b': b,
        'c': c,
        'p': p,
    }
    return render(request, 'books/all_books.html', context)


def register_new_category(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = BookCategoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "The new Category was successfully added to the database")
        return redirect(reverse('books:list'))
    context = {
        "form": form,
    }
    return render(request, "books/register_category.html", context)


def register_new_publisher(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = BookPublisherForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "The new Publisher was successfully added to the database")
        return redirect(reverse('books:list'))
    context = {
        "form": form,
    }
    return render(request, "books/register_publisher.html", context)


def register_new_book(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = RegisterBookForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "The book was successfully added to the records")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "book_register.html", context)


def book_detail(request, slug=None):
    instance = get_object_or_404(Book, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.description)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }
    return render(request, "book_detai.html", context)


def book_list(request):
    today = timezone.now().date()
    queryset_list = Book.objects.active()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Book.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(borower__reg_no__icontains=query) |
            Q(no__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "book_list.html", context)


def book_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Book, slug=slug)
    form = RegisterBookForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "The book details were successfully saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "book_register.html", context)


def borrow_book(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Book, slug=slug)
    form = BorrowBookForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "The book status has been successfully changed", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "books/borrow_book.html", context)


def book_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Book, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("books:list")





