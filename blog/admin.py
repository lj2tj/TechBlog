from django.contrib import admin

# Register your models here.
from .models_article import Category, Article
from .models_website import GlobalConfig
from .models_account import UserProfile, MyTech

admin.site.register(Category)
admin.site.register(Article)

admin.site.register(GlobalConfig)
admin.site.register(UserProfile)

class MyTechAdmin(admin.ModelAdmin):
        list_display = ('name', 'proficiency') 

admin.site.register(MyTech, MyTechAdmin)