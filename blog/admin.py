from django.contrib import admin

# Register your models here.
from .models_article import Category, Article, Comment
from .models_website import GlobalConfig
from .models_account import UserProfile, MyTech, AccountComment

admin.site.site_header = "博客后台管理系统"
admin.site.site_title = "博客后台管理系统"

admin.site.register(GlobalConfig)

#Article related
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        list_display = ('name', 'description') 

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
        list_display = ('title', 'category', 'status', 'is_top')
        ordering = ("status", "-created_time", "-likes")
        search_fields = ("title",)
        list_per_page = 20

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
        list_display = ('article', 'user_name', 'user_email') 
        search_fields = ("article__title",)
        list_per_page = 20

#User related
@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
        list_display = ('user',) 

@admin.register(MyTech)
class MyTechAdmin(admin.ModelAdmin):
        list_display = ('name', 'proficiency')

@admin.register(AccountComment)
class ACAdmin(admin.ModelAdmin):
        list_display = ('user_name', 'user_email', 'comment_to')
        list_per_page = 20