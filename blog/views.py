from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models_article import Category, Article, Comment
from .models_account import UserProfile, MyTech, AccountComment
from .models_website import GlobalConfig

# Create your views here.

def index(request):
    config = GlobalConfig.objects.all()[0]
    categories = Category.objects.all()
    hot_articles = Article.objects.filter(status='p').order_by("-likes", "-views", "created_time")[:5]

    context = {
        "config" : config,
        "category_list" : categories,
        "hot_articles" : hot_articles
    }
    return render(request, "index.html", context=context)

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

def like_article(request, article_id):
    article = Article.objects.filter(id=article_id)
    if article:
        try:
            count = article[0].likes
            article[0].likes = count + 1
            article[0].save()
            return HttpResponse(str(article[0].likes))
        except Exception as e:
            return HttpResponse("-1")
    else:
        return HttpResponse("-1")

def article(request, article_id):
    config = GlobalConfig.objects.all()[0]
    categories = Category.objects.all()

    articles = Article.objects.filter(id=article_id, status='p')

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

def like_tech(request, tech_id):
    tech = MyTech.objects.filter(id=tech_id)
    if tech:
        try:
            count = tech[0].nice_count
            tech[0].nice_count = count + 1
            tech[0].save()
            count = count + 1
            return HttpResponse(str(count))
        except Exception as e:
            return HttpResponse("-1")
    else:
        return HttpResponse("-1")

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

def accountcomment(request, comment_to):
    user_name = request.POST.get('user_name', '')
    user_email = request.POST.get('user_email', '')
    comment = request.POST.get('comment', '')

    if user_name and user_email and comment:
        try:
            ac = AccountComment()
            ac.user_name = user_name
            ac.user_email = user_email
            ac.body = comment
            ac.comment_to = comment_to
            ac.save()
            return HttpResponse(str(ac.id))
        except Exception as e:
            return HttpResponse("-1")
    else:
        return HttpResponse("-1")
    pass

def about(request):
    config = GlobalConfig.objects.all()[0]
    categories = Category.objects.all()
    author = UserProfile.objects.all()[0]
    my_tech = MyTech.objects.all()
    ac = AccountComment.objects.all().order_by("-id")

    context = {
        "config" : config,
        "category_list" : categories,
        "author" : author,
        "my_tech" : my_tech,
        "comments" : ac
    }

    return render(request, "about.html", context=context)