from django.conf.urls import url

from .views import (
    all_students, register_new_parent, register_new_student, delete_student, student_update, student_detail

)

urlpatterns = [
    url(r'^$', all_students, name='home'),
    url(r'^add-student/$', register_new_student, name='add-student'),
    url(r'^add-parent/$', register_new_parent, name='add-parent'),
    url(r'^(?P<slug>[\w-]+)/$', student_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', student_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', delete_student),
]
