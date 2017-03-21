from django.contrib import admin

from .models import Day, Year, Time, Subject, \
    Teacher, Timetable, AccademicEvent, \
    EndTermExamPerformance

admin.site.register(EndTermExamPerformance)
admin.site.register(Year)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Time)
admin.site.register(Day)
admin.site.register(Timetable)
admin.site.register(AccademicEvent)
