# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 16:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import library.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.DateField()),
                ('draft', models.BooleanField(default=False)),
                ('no', models.CharField(default=0, max_length=20)),
                ('description', models.TextField()),
                ('reg_date', models.DateField(auto_now_add=True)),
                ('borrowed', models.BooleanField(default=False)),
                ('borrow_or_return_date', models.DateTimeField(auto_now=True)),
                ('borrower', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-reg_date', '-borrower'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=library.models.upload_location, width_field='width_field')),
                ('width_field', models.IntegerField(default=0)),
                ('height_field', models.IntegerField(default=0)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('post_address', models.CharField(max_length=255)),
                ('email', models.EmailField(default='publisher@example.com', max_length=254)),
                ('phone', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('reg_no', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Publisher'),
        ),
    ]