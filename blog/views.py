#!/usr/bin/env python
#coding=utf-8

import os
import json
import markdown2
from datetime import *
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.template import RequestContext, loader
from django.conf import settings
from django.contrib import auth
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User
from blog.models import Article, Category, Tag, UserProfile, WebSiteAbout
from .models import BlogComment, AppSettings, WebSiteConfig
from .forms import CustomeLoginForm, BlogCommentForm, ArticleEditForm
from django.http import StreamingHttpResponse, HttpResponse, HttpRequest, request

WebSiteInfo = WebSiteConfig()

def GetWebSiteInfo():
    """
    Get web site configuration information.
    """
    if len(AppSettings.objects.filter(name='WebSiteName')) > 0:
        WebSiteInfo.WebSiteName = AppSettings.objects.filter(name='WebSiteName')[0].value
    if len(AppSettings.objects.filter(name='ICP')) > 0:
        WebSiteInfo.ICP = AppSettings.objects.filter(name='ICP')[0].value
    if len(AppSettings.objects.filter(name='Copyright')) > 0:
        WebSiteInfo.Copyright = AppSettings.objects.filter(name='Copyright')[0].value
    if len(AppSettings.objects.filter(name='Address')) > 0:
        WebSiteInfo.Address = AppSettings.objects.filter(name='Address')[0].value
    if len(AppSettings.objects.filter(name='Phone')) > 0:
        WebSiteInfo.Phone = AppSettings.objects.filter(name='Phone')[0].value

class About(ListView):
    """
    Website about page.
    """

    template_name = 'blog/about.html'

    def get_queryset(self):
        settings = WebSiteAbout.objects.all()
        return settings

    def get_context_data(self, **kwargs):
        GetWebSiteInfo()
        kwargs['WebSiteInfo'] = WebSiteInfo
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['settings'] = WebSiteAbout.objects.all()
        return super(About, self).get_context_data(**kwargs)


class IndexView(ListView):
    """
    The index page, show all artiicles.
    """

    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')[:10]
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        GetWebSiteInfo()
        kwargs['WebSiteInfo'] = WebSiteInfo
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['display'] = "l"
        kwargs['tag_list'] = Tag.objects.all().order_by('created_time')
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    """
    Article detail view, this view will display all the detail information of an article.
    """

    model = Article
    template_name = "blog/detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        obj.views += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        GetWebSiteInfo()
        kwargs['WebSiteInfo'] = WebSiteInfo
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        return super(ArticleDetailView, self).get_context_data(**kwargs)

def NewArticle(request):
    """
    Create new article page.
    """
    category_list = Category.objects.all().order_by('created_time')
    tag_list = Tag.objects.all().order_by('created_time')
    GetWebSiteInfo()
    dic = {'category_list':category_list, 'tag_list': tag_list, 'WebSiteInfo': WebSiteInfo}
    return render(request, "blog/add_article.html", dic)

def EditArticle(request, article_id):
    """
    Edit existing article page.
    """
    category_list = Category.objects.all().order_by('created_time')
    tag_list = Tag.objects.all().order_by('created_time')
    article = Article.objects.get(id=article_id)

    GetWebSiteInfo()
    dic = {'category_list':category_list, 'tag_list': tag_list, 'article': article, 'WebSiteInfo': WebSiteInfo}
    return render(request, "blog/edit_article.html", dic)


def GetArticles(request):
    """
    Get articles with given option.
    """
    articles = []
    limit = int(request.GET.get('limit', '10'))
    offset = int(request.GET.get('offset', '0'))
    searchText = request.GET.get('searchText', '')
    
    sortName = request.GET.get('sortName', '')
    if len(sortName) <= 0:
        sortName = 'created_time'

    sortOrder = request.GET.get('sortOrder', '')
    if sortOrder == "desc":
        sortName = "-" + sortName
    
    cate_id = int(request.GET.get('cate_id', '-1'))

    if cate_id > -1:
        articles = Article.objects.filter(status="p", title__contains=searchText, category=cate_id).order_by(sortName)
    else:
        articles = Article.objects.filter(status="p", title__contains=searchText).order_by(sortName)
    
    return HttpResponse(json.dumps({ "total" : len(articles), "rows" : queryset_to_json(articles[offset:(offset+limit)])}))

def UpdateArticle(request, article_id):
    """
    Update an existing article.     
    """
    if not request.user.is_authenticated():
        return render_to_response("user/login.html", RequestContext(request))

    if request.method == 'POST':
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')
        status = request.POST.get('status', '')
        topped = request.POST.get('topped', '')
        attachment = request.POST.get('attachment', '')
        category = request.POST.get('category', '')
        tag = request.POST.get('tag', '')


        article = Article.objects.get(id=article_id)
        article.title = title
        article.body = body
        article.status = status
        article.topped = topped
        article.attachment = attachment
        article.category = Category.objects.filter(id=category)[0]
        article.tag = Tag.objects.filter(id=tag)[0]
        article.user = User.objects.filter(id=request.user.id)[0]
        article.save()

        article_id = Article.objects.filter(title=title, status=article.status, category=article.category, tag=article.tag)[0]
        url = "/article/" + str(article_id.id)
        print(url)
        return HttpResponseRedirect(url)

class CategoryView(ListView):
    """
    Show all files in a category.
    """

    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')[:10]
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        GetWebSiteInfo()
        kwargs['WebSiteInfo'] = WebSiteInfo
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['display'] = Category.objects.filter(id=self.kwargs['cate_id'])[0].display
        kwargs['tag_list'] = Tag.objects.all().order_by('created_time')
        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(ListView):
    """
    Show all files with same tag name.
    """

    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        #???
        kwargs['settings'] = AppSettings.objects.all()
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['tag_list'] = Tag.objects.filter(id=self.kwargs['tag_id']).order_by('name')
        return super(TagView, self).get_context_data(**kwargs)


class CommentPostView(FormView):
    """
    Comment post view.
    """

    form_class = BlogCommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.article = target_article
        comment.save()
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        return render(self.request, 'blog/detail.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.blogcomment_set.all(),
        })


class AdminEditArticalView(FormView):
    form_class = ArticleEditForm
    template_name = 'admin/editArticle.html'
    context_object_name = "article"
    def get_queryset(self):
        id = int(self.kwargs['article_id'])
        article = Article.objects.get(id=id)
        article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article
    pass





def queryset_to_json(queryset):  
    obj_arr=[]  
    for o in queryset:  
            obj_arr.append(o.toDict())  
    return obj_arr 

def json_item_to_string(obj): 
    obj_arr=[]
    for o in obj:
        serialized = dict([(attr, str(o[attr])) for attr in [f for f in o]])
        obj_arr.append(serialized) 
    return obj_arr