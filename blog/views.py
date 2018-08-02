from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse

from .models_article import Category, Article, Comment
from .models_account import UserProfile
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
        "comments" : comments
    }
    return render(request, "article.html", context=context)

def like(request, article_id):

    pass


def about(request):
    config = GlobalConfig.objects.all()[0]
    categories = Category.objects.all()
    author = UserProfile.objects.all()[0]

    context = {
        "config" : config,
        "category_list" : categories,
        "author" : author
    }

    return render(request, "about.html", context=context)