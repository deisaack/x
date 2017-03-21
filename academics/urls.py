from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.academics_home, name='all'),
    url(r'^t/$', views.mega_timetable, name='timetable'),
    url(r'^r/$', views.full_result, name='result'),
    url(r'^ac/(?P<slug>[\w-]+)/$', views.time_item_detail, name='time-item'),
    url(r'^import_result/$', views.import_sheet, name="import_sheet"),
    url(r'^export_result/(.*)', views.export_data, name="export")
]
