from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify

from django.utils import timezone
from academics.models import EndTermExamPerformance, Year


class StudentManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(StudentManager, self).filter(draft=False).filter(publish__lte=timezone.now())



def upload_location(instance, filename):
    return "%s/%s" % (id, filename)


class Parent(models.Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    id_no = models.IntegerField(help_text='Your National ID Number', null=True, blank=True, unique=True)
    email = models.EmailField(default='parent@example.com')
    phone = models.IntegerField(null=True, blank=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    residence = models.CharField(max_length=100, default='Kaborom')
    profession = models.CharField(max_length=255, default='', null=True, blank=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Rank(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="About this rank ...")

    def __str__(self):
        return self.title


class Staff(models.Model):
    user_acc = models.OneToOneField(User)
    staff_no = models.CharField(max_length=30, unique=True, primary_key=True)
    id_no = models.IntegerField(help_text='Your National ID Number', null=True, blank=True)
    email = models.EmailField(default='staff@example.com')
    phone = models.IntegerField(null=True, blank=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    residence = models.CharField(max_length=100, default='Kaborom')
    level_of_study = models.CharField(max_length=255, default='', null=True, blank=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    rank = models.ManyToManyField(Rank, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "%s %s" % (self.staff_no, self.user)


class Student(models.Model):
    user_acc = models.OneToOneField(User)
    reg_no = models.CharField(max_length=30, unique=True, primary_key=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    residence = models.CharField(max_length=100, default='Kaborom')
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    parent = models.ForeignKey(Parent, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    year_of_study = models.ForeignKey(Year, null=True, blank=True)
    exam = models.ForeignKey(EndTermExamPerformance, null=True, blank=True)
    slug = models.SlugField(unique=False, null=True, blank=True)

    objects = StudentManager()

    def __unicode__(self):
        return self.user_acc.first_name

    def __str__(self):
        return self.user_acc.first_name

    def get_absolute_url(self):
        return reverse("administration:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-year_of_study", "-timestamp"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.user_acc)
    if new_slug is not None:
        slug = new_slug
    qs = Student.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_book_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_book_receiver, sender=Student)
