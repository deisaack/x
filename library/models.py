from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify


class BookManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(BookManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    BookModel = instance.__class__
    return "%s/%s" % (id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_location,
            null=True,
            blank=True,
            width_field="width_field",
            height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    post_address = models.CharField(max_length=255)
    email = models.EmailField(default='publisher@example.com')
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    reg_no = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)

    def __str__(self):
        return self.reg_no


class Book(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    publish = models.DateField(auto_now_add=False)
    draft = models.BooleanField(default=False)
    no = models.CharField(max_length=20, default=000000)
    category = models.ForeignKey(Category)
    publisher = models.ForeignKey(Publisher)
    description = models.TextField()
    reg_date = models.DateField(auto_now_add=True)
    borrowed = models.BooleanField(default=False)
    borrower = models.OneToOneField(User, on_delete=None, null=True, blank=True)
    borrow_or_return_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = BookManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-reg_date", "-borrower"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Book.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_book_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_book_receiver, sender=Book)
