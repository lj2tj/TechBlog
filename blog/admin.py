from django.contrib import admin

# Register your models here.
from .models_article import Category, Article
from .models_website import GlobalConfig
from .models_account import UserProfile

admin.site.register(Category)
admin.site.register(Article)

admin.site.register(GlobalConfig)
admin.site.register(UserProfile)