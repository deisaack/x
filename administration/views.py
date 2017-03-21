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

from .forms import RegisterNewParent, RegisterNewStudent
from portals.models import Student
from academics.models import Year


def all_students(request):
    queryset_list = Student.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Student.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(reg_no__icontains=query)
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

    b = Student.objects.all().count()  # .order_by("-timestamp")
    y = Year.objects.all().count()
    context = {
        "object_list": queryset,
        "title": "Our Students",
        "page_request_var": page_request_var,
        'b': b,
        'y': y,
    }
    return render(request, 'administration/all_students.html', context)


def register_new_student(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = RegisterNewStudent(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "The new Student was successfully added to the database")
        return redirect(reverse('administration:home'))
    context = {
        "form": form,
    }
    return render(request, "administration/register.html", context)


def register_new_parent(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = RegisterNewParent(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "The new Parent was successfully added to the database")
        return redirect(reverse('administration:home'))
    context = {
        "form": form,
    }
    return render(request, "administration/register.html", context)


def student_detail(request, slug=None):
    instance = get_object_or_404(Student, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.description)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }
    return render(request, "administration/student_detail.html", context)


def student_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Student, slug=slug)
    form = RegisterNewStudent(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "The student details were successfully saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "administration/register.html", context)



def delete_student(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Student, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("books:list")


# def update_exam_result(request):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#
#     form = RegisterBookForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.save()
#         # message success
#         messages.success(request, "The book was successfully added to the records")
#         return HttpResponseRedirect(instance.get_absolute_url())
#     context = {
#         "form": form,
#     }
#     return render(request, "book_register.html", context)


