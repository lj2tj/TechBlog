# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('value', models.CharField(max_length=100, null=True, verbose_name=b'\xe6\x98\xbe\xe7\xa4\xba\xe5\x80\xbc')),
                ('comment', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\xb3\xa8\xe9\x87\x8a', blank=True)),
            ],
            options={
                'verbose_name': '\u7f51\u7ad9\u914d\u7f6e',
                'verbose_name_plural': '\u7f51\u7ad9\u914d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=70, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('body', tinymce.models.HTMLField(verbose_name=b'\xe6\xad\xa3\xe6\x96\x87')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('status', models.CharField(max_length=1, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe7\x8a\xb6\xe6\x80\x81', choices=[(b'd', b'Draft'), (b'p', b'Published')])),
                ('views', models.PositiveIntegerField(default=0, verbose_name=b'\xe6\xb5\x8f\xe8\xa7\x88\xe9\x87\x8f', editable=False)),
                ('likes', models.PositiveIntegerField(default=0, verbose_name=b'\xe7\x82\xb9\xe8\xb5\x9e\xe6\x95\xb0', editable=False)),
                ('topped', models.BooleanField(default=False, verbose_name=b'\xe7\xbd\xae\xe9\xa1\xb6')),
            ],
            options={
                'ordering': ['-last_modified_time'],
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120, verbose_name=b'\xe9\x99\x84\xe4\xbb\xb6\xe5\x90\x8d')),
                ('attachment', models.FileField(upload_to=b'Articles', verbose_name=b'\xe9\x99\x84\xe4\xbb\xb6')),
                ('upload_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x97\xb6\xe9\x97\xb4')),
                ('download_times', models.PositiveIntegerField(default=0, verbose_name=b'\xe4\xb8\x8b\xe8\xbd\xbd\xe6\xac\xa1\xe6\x95\xb0', editable=False)),
            ],
            options={
                'verbose_name': '\u9644\u4ef6',
                'verbose_name_plural': '\u9644\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=100, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe8\x80\x85\xe5\x90\x8d\xe5\xad\x97')),
                ('user_email', models.EmailField(max_length=255, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe8\x80\x85\xe9\x82\xae\xe7\xae\xb1')),
                ('body', tinymce.models.HTMLField(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\x86\x85\xe5\xae\xb9')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\x8f\x91\xe8\xa1\xa8\xe6\x97\xb6\xe9\x97\xb4')),
                ('article', models.ForeignKey(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe6\x89\x80\xe5\xb1\x9e\xe6\x96\x87\xe7\xab\xa0', to='blog.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'\xe7\xb1\xbb\xe5\x90\x8d')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('display', models.CharField(default=b'l', max_length=1, verbose_name=b'\xe6\x98\xbe\xe7\xa4\xba\xe6\x96\xb9\xe5\xbc\x8f', choices=[(b'l', b'List'), (b'D', b'Detail')])),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe\xe5\x90\x8d')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(height_field=120, upload_to=b'', width_field=100, null=True, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('mobile_phone', models.CharField(max_length=20, null=True, verbose_name=b'\xe7\xa7\xbb\xe5\x8a\xa8\xe7\x94\xb5\xe8\xaf\x9d')),
                ('location', models.CharField(max_length=200, null=True, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80')),
                ('user', models.OneToOneField(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7ad9\u957f',
                'verbose_name_plural': '\u7ad9\u957f',
            },
        ),
        migrations.CreateModel(
            name='WebSiteAbout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('value', models.CharField(max_length=100, null=True, verbose_name=b'\xe6\x98\xbe\xe7\xa4\xba\xe5\x80\xbc')),
                ('comment', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\xb3\xa8\xe9\x87\x8a', blank=True)),
            ],
            options={
                'verbose_name': '\u7f51\u7ad9\u4ecb\u7ecd',
                'verbose_name_plural': '\u7f51\u7ad9\u4ecb\u7ecd',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='attachment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe9\x99\x84\xe4\xbb\xb6', to='blog.Attachment', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb', to='blog.Category', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ForeignKey(verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe\xe9\x9b\x86\xe5\x90\x88', blank=True, to='blog.Tag', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
