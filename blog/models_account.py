from django.db import models
from django.contrib.auth.models import User

from tinymce.models import HTMLField

class UserProfile(models.Model):
    """
    User profile class.
    """

    user = models.OneToOneField(User, unique=True, verbose_name=('作者'), on_delete=models.CASCADE)
    #photo = models.ImageField("头像", width_field=100, height_field=120, null=True)
    about = HTMLField('站长介绍')
    qq = models.CharField('qq', max_length=20, null=True, blank=True)
    toutiao = models.CharField('头条号', max_length=20, null=True, blank=True)
    github = models.CharField('github', max_length=100, null=True, blank=True)
    location = models.CharField('地址', max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'account_owner'
        verbose_name = "作者"
        verbose_name_plural = verbose_name

class MyTech(models.Model):
    """
    Technique that I known, like: C#, Python...
    """

    name = models.CharField("技能名称", max_length=20, null=False, blank=False)
    proficiency = models.IntegerField("熟练程度", max_length=2, default=5)
    nice_count = models.IntegerField("点赞数", max_length=10, default=0)

    class Meta:
        verbose_name = "技能"
        verbose_name_plural = verbose_name