"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path("index/", views.index),
    path("category/<int:category_id>/<int:page_index>/", views.category, name="category"),
    path("article/<int:article_id>/", views.article, name="article"),
    path("addcomment/<int:article_id>/", views.addcomment, name="addcomment"),
    path("about/", views.about, name="about"),
    path("liketech/<int:tech_id>/", views.like_tech, name="like_tech"),
]
