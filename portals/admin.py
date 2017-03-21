from django.contrib import admin

from .models import Parent, Student, Staff, Rank

admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Rank)
