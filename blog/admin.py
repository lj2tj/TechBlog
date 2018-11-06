from django.contrib import admin

# Register your models here.
from .models_article import Category, Article, Comment
from .models_website import GlobalConfig
from .models_account import UserProfile, MyTech, AccountComment

admin.site.register(GlobalConfig)

#Article related
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        list_display = ('name', 'description') 

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
        list_display = ('title', 'category', 'status')
        ordering = ("status", "-created_time", "-likes")
        list_per_page = 20

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
        list_display = ('article', 'user_name', 'user_email') 

#User related
@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
        list_display = ('user',) 

@admin.register(MyTech)
class MyTechAdmin(admin.ModelAdmin):
        list_display = ('name', 'proficiency')

@admin.register(AccountComment)
class ACAdmin(admin.ModelAdmin):
        list_display = ('user_name', 'user_email')
        list_per_page = 20