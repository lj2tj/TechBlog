#!/usr/bin/env python
#coding=utf-8

import os
import json
from datetime import datetime
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.template import RequestContext, loader
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from blog.models import UserProfile, BlogComment, AppSettings
from blog.models import Article, Category, Tag
from blog.views import WebSiteInfo, GetWebSiteInfo
from django.http import StreamingHttpResponse, HttpResponse


def UpdateUserInfo(request):
    """
    Update user info.
    """
    try:
        if not request.user.is_authenticated():
            return render_to_response("user/login.html", \
            RequestContext(request, {"WebSiteInfo" : WebSiteInfo}))

        user = User.objects.filter(id=request.user.id)[0]
        
        email = request.GET.get('email', '')
        if len(email) > 0:
            if email.find("@") <= 0:
                return HttpResponse("邮箱地址不正确")
            else:
                user.email = email
                user.save()
        
        mobile_phone = request.GET.get('mobile_phone', '')
        position = request.GET.get('position', '')
        title = request.GET.get('jobTitle', '')
        location = request.GET.get('location', '')

        if len(mobile_phone) > 0 or len(position) > 0 or len(title) > 0 or len(location) > 0:
            profile = UserProfile.objects.filter(user=request.user.id)

            editProfile = None
            if profile is None or len(profile) <= 0:
                editProfile = UserProfile()
            else:
                editProfile = profile[0]
            editProfile.user_id = request.user.id
            editProfile.mobile_phone = mobile_phone
            editProfile.location = location
            editProfile.website_level = WebSiteLevel.objects.get(id=1)
            editProfile.save()

        return HttpResponse("1")
    except Exception, e:
        return HttpResponse(e)

def ValidateUserName(request):
    """
    Validate if an user already exists when registering a new user,
    if yes return alert message, else retuan 1.
    """
    name = request.GET.get('name', '')
    if name == '':
        return HttpResponse("Empty user name error!")
    else:
        user = User.objects.filter(username=name)
        if user is None or user.__len__() == 0:
            return HttpResponse('1')
        else:
            return HttpResponse('User [%s] already exists' % name)


def loginPage(request):
    """
    User login page.
    """
    GetWebSiteInfo()
    category_list = Category.objects.all().order_by('created_time')
    return render_to_response("user/login.html", \
        RequestContext(request, {"WebSiteInfo" : WebSiteInfo, "category_list" : category_list}))


def login(request):
    """
    Customer login.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect("usercenter")
    else:
        if request.method == 'POST':
            username = request.POST.get('memUserId', '')
            password = request.POST.get('memPassword', '')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("usercenter")

    category_list = Category.objects.all().order_by('created_time')
    return render_to_response("user/login.html", \
        RequestContext(request, {"WebSiteInfo" : WebSiteInfo, "category_list" : category_list}))


def UserCenter(request):
    """
    Website user center.
    """
    GetWebSiteInfo()

    if not request.user.is_authenticated():
        return render_to_response("user/login.html", RequestContext(request))

    category_list = Category.objects.all().order_by('created_time')
    uploaded_files = Article.objects.filter(user_id=request.user.id)
    if not any(uploaded_files):
        uploaded_files = []

    profile = UserProfile.objects.filter(user=request.user.id)
    
    myProfile = None
    if len(profile) <= 0:
        myProfile = UserProfile()
    else:
        myProfile = profile[0] 

    dic = {'category_list':category_list, \
    'base_info': request.user, \
    'WebSiteInfo' : WebSiteInfo, \
    'profile': myProfile}
    return render(request, "user/usercenter.html", dic)


def Download(request, article_id):
    """
    Download a document.
    """
    
    if not article_id:
        return HttpResponse('Invalid file.')

    upload_file_path = settings.MEDIA_ROOT

    if upload_file_path is None:
        return HttpResponse('System setting error, upload_file_path is empty.')

    article = Article.objects.filter(id=article_id)[0]

    article.download += 1
    article.save()

    file_full_name = os.path.join(upload_file_path, unicode(article.attachment))
    print file_full_name

    response = StreamingHttpResponse(file_iterator(file_full_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(article.attachment)
    return response


def logout(request):
    """
    Logout website.
    """
    auth.logout(request)
    return HttpResponseRedirect("/")



def file_iterator(file_name, chunk_size=512):
    """File downloader"""
    with open(file_name,'rb') as new_file:
        while True:
            block = new_file.read(chunk_size)
            if block:
                yield block
            else:
                break
