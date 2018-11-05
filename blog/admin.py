from django.contrib import admin

# Register your models here.
from .models_article import Category, Article
from .models_website import GlobalConfig
from .models_account import UserProfile, MyTech, AccountComment

class CategoryAdmin(admin.ModelAdmin):
        list_display = ('name', 'description') 
admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
        list_display = ('title', 'category', 'status') 
admin.site.register(Article, ArticleAdmin)

admin.site.register(GlobalConfig)

class UserAdmin(admin.ModelAdmin):
        list_display = ('user',) 
admin.site.register(UserProfile, UserAdmin)

class MyTechAdmin(admin.ModelAdmin):
        list_display = ('name', 'proficiency') 
admin.site.register(MyTech, MyTechAdmin)

class ACAdmin(admin.ModelAdmin):
        list_display = ('user_name', 'user_email') 
admin.site.register(AccountComment, ACAdmin)