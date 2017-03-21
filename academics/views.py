try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except:
    pass
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Timetable, AccademicEvent, EndTermExamPerformance
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django import forms
import django_excel as excel



data = [
    [1, 2, 3],
    [4, 5, 6]
]


class UploadFileForm(forms.Form):
    file = forms.FileField()


def export_data(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_table(
            EndTermExamPerformance, 'xls', file_name="sheet")
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these " +
            "in your url suffix: sheet, book or custom")


def import_sheet(request):
    students = EndTermExamPerformance.objects.all()
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                name_columns_by_row=1,
                model=EndTermExamPerformance,
                mapdict=['reg_no', 'first_name', 'last_name', 'mathematics',
                         'english', 'kiswahili', 'science', 'sst_cre', 'total'])
            return  redirect(reverse('academics:all'))
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {'form': form, 'students': students})


















def time_item_detail(request, slug=None):
    instance = get_object_or_404(Timetable, slug=slug)
    context = {
        "title": instance.year,
        "instance": instance,
    }
    return render(request, 'academics/time_item_detail.html', context)



def full_result(request):
    results = EndTermExamPerformance.objects.order_by('total')
    context = {
        "title": "Full result",
        'results': results
    }
    return render(request, "academics/academics_home.html", context)


def mega_timetable(request):
    today = timezone.now().date()
    queryset_list = Timetable.objects.order_by('day', 'time', 'year')  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Timetable.objects.order_by('day', 'time', 'year')  # .order_by("-timestamp")

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(slug__icontains=query) |
            Q(subject__name__icontains=query) |
            Q(year__name__icontains=query) |
            Q(day__name__icontains=query) |
            Q(teacher__first_name__icontains=query) |
            Q(teacher__last_name__icontains=query) |
            Q(time__name__icontains=query)
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
    context = {
        "object_list": queryset,
        "title": "Megatimetable",
        "today": today,
    }
    return render(request, "academics/academics_home.html", context)


def academics_home(request):
    today = timezone.now().date()
    queryset_list = Timetable.objects.order_by('day', 'time', 'year')  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Timetable.objects.order_by('day', 'time', 'year')  # .order_by("-timestamp")

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(slug__icontains=query) |
            Q(subject__name__icontains=query) |
            Q(year__name__icontains=query) |
            Q(day__name__icontains=query) |
            Q(teacher__first_name__icontains=query) |
            Q(teacher__last_name__icontains=query) |
            Q(time__name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 5)  # Show 25 contacts per page
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


    results = EndTermExamPerformance.objects.order_by('total')[:5]
    events = AccademicEvent.objects.order_by('-timestamp')[:3]
    context = {
        "object_list": queryset,
        "title": "Welcome to Holistic Accademy Accademics Department",
        # "page_request_var": page_request_var,
        "today": today,
        'events': events,
        'results': results

    }
    return render(request, "academics/academics_home.html", context)

