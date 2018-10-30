from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models_article import Category, Article, Comment
from .models_account import UserProfile, MyTech
from .models_website import GlobalConfig

# Create your views here.

def index(request):
    config = GlobalConfig.objects.all()[0]
    categories = Category.objects.all()

    context = {
        "config" : config,
        "category_list" : categories
    }
    return render(request, "base.html", context=context)

def category(request, category_id, page_index):
    # page size = 10
    page_size = 10

    config = GlobalConfig.objects.all()[0]
    categories = Category.objects.all()

    
    all_articles = Article.objects.filter(status='p', category_id=category_id)

    articles = None
    if page_index < 0:
        articles = all_articles[:page_size]
    elif page_index > (len(all_articles) // page_size):
        articles = all_articles[-10:-1]
    else:
        start = page_index * page_size
        articles = all_articles[start:(start+10)]
    

    context = {
        "config" : config,
        "category_list" : categories,
        "articles" : articles
    }
    return render(request, "category.html", context=context)

def article(request, article_id):
    config = GlobalConfig.objects.all()[0]
    categories = Category.objects.all()

    articles = Article.objects.filter(id=article_id)

    article = None
    comments = None
    if len(articles) > 0:
        article = articles[0]
        article.views = int(article.views) + 1
        article.save()

        comments = Comment.objects.filter(article_id=article_id)
    else:
        return Http404()

    context = {
        "config" : config,
        "category_list" : categories,
        "article" : article,
        "comments" : comments,
        "user_name" : request.session.get('user_name', ''), 
        "user_email" : request.session.get('user_email', ''), 
        "comment_editor" : request.session.get('comment_editor', '')
    }

    request.session['user_name'] = ''
    request.session['user_email'] = ''
    request.session['comment_editor'] = ''

    return render(request, "article.html", context=context)

def like(request, article_id):

    pass

def addcomment(request, article_id):
    user_name = request.POST.get('user_name', '')
    user_email = request.POST.get('user_email', '')
    comment_editor = request.POST.get('comment_editor_hidden', '')

    if user_name and user_email and comment_editor:
        comment = Comment()
        comment.user_name = user_name
        comment.user_email = user_email
        comment.body = comment_editor
        comment.article = Article.objects.get(id=article_id)
        comment.save()

        return HttpResponseRedirect('/blog/article/%d/' % article_id)
    else:
        request.session['user_name'] = user_name
        request.session['user_email'] = user_email
        request.session['comment_editor'] = comment_editor
        return article(request, article_id)
    pass

def about(request):
    config = GlobalConfig.objects.all()[0]
    categories = Category.objects.all()
    author = UserProfile.objects.all()[0]
    my_tech = MyTech.objects.all()

    context = {
        "config" : config,
        "category_list" : categories,
        "author" : author,
        "my_tech" : my_tech
    }

    return render(request, "about.html", context=context)