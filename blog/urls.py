#!/usr/bin/env python
#coding=utf-8

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from blog import views, viewUser

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?i)article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^(?i)Download/attachment$', viewUser.Download, name='Download'),
    url(r'^(?i)GetArticles$', views.GetArticles, name='GetArticles'),
    url(r'^(?i)NewArticle$', login_required(views.NewArticle), name='NewArticle'),
    url(r'^(?i)EditArticle/(?P<article_id>\d+)$', login_required(views.EditArticle), name='EditArticle'),
    url(r'^(?i)AddArticle$', login_required(views.AddArticle), name='AddArticle'),
    url(r'^(?i)UpdateArticle/(?P<article_id>\d+)$', login_required(views.UpdateArticle), name='UpdateArticle'),
    url(r'^(?i)category/(?P<cate_id>\d+)$', views.CategoryView.as_view(), name='category'),
    url(r'^(?i)tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    url(r'^(?i)article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), \
    name='comment'),
    url(r'^(?i)about$', views.About.as_view(), name='about'),
    url(r'^(?i)usercenter$', login_required(viewUser.UserCenter), name='usercenter'),
    url(r'^(?i)UpdateUserInfo$', login_required(viewUser.UpdateUserInfo), name='UpdateUserInfo'),
    url(r'^(?i)ValidateUserName$', viewUser.ValidateUserName, name='ValidateUserName'),
    url(r'^(?i)login$', viewUser.login, name='login'),
    url(r'^(?i)logout$', viewUser.logout, name='logout'),
    url(r'^(?i)loginpage$', viewUser.loginPage, name='LoginPage'),
]
