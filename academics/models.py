from __future__ import unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify

class TimetableManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(TimetableManager, self)


def upload_location(instance, filename):
    BookModel = instance.__class__
    return "%s/%s" %(id, filename)

class AccademicEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    def __str__(self):
        return self.title


class Day(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Year(models.Model):
    name = models.CharField(max_length=15)
    students = models.IntegerField(default=0)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Time(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    time = models.TimeField(unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Teacher(models.Model):
    tch_no = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name

class Timetable(models.Model):
    name = models.CharField(max_length=20, null=True)
    day = models.ForeignKey(Day)
    year = models.ForeignKey(Year)
    time = models.ForeignKey(Time)
    subject = models.ForeignKey(Subject)
    teacher = models.ForeignKey(Teacher)
    slug = models.SlugField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("academics:time-item", kwargs={"slug": self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Timetable.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_academic_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_academic_receiver, sender=Timetable)



class EndTermExamPerformance(models.Model):
    reg_no = models.CharField(max_length=20, unique=True, primary_key=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    mathematics = models.IntegerField(null=True, blank=True)
    english = models.IntegerField(null=True, blank=True)
    kiswahili = models.IntegerField(null=True, blank=True)
    science = models.IntegerField(null=True, blank=True)
    sst_cre = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.reg_no


